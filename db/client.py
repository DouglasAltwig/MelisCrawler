"""PostgreSQL Database Module"""
from __future__ import annotations
from psycopg2.extras import RealDictCursor
import psycopg2


class Client():
    """Database client"""

    def __init__(self, host:str, database:str, user:str, password:str) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def load_token(self) -> dict:
        """Loads the latest token from the database
            Returns: 
                A dict
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            postgres_read_query = """
                SELECT 
                    access_token, token_type, expires_in, scope, user_id, refresh_token, expires_at 
                FROM oauth_token 
                ORDER BY expires_at DESC 
                LIMIT 1;
            """
            cur.execute(postgres_read_query)
            return dict(cur.fetchone())

        except (psycopg2.Error) as error:
            print(f"Failed to read from 'oauth_token' table: {error}")
        finally:
            if conn:
                cur.close()
                conn.close()


    def save_token(self, token: dict) -> dict:
        """Persists token to the database
            Args:
                token:
            Returns:
                A dict
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
            cur = conn.cursor()
            sql_insert_query = """
            INSERT INTO oauth_token 
                (access_token, token_type, expires_in, scope, user_id, refresh_token, expires_at) 
            VALUES 
                (%s,%s,%s,%s,%s,%s,%s)
            """
            record_to_insert = (
                token['access_token'],
                token['token_type'],
                token['expires_in'],
                token['scope'],
                token['user_id'],
                token['refresh_token'],
                token['expires_at'])

            cur.execute(sql_insert_query, record_to_insert)
            conn.commit()
            return token
        except (psycopg2.Error) as error:
            print(f"Failed to insert records into 'oauth_token' table: {error}")
        finally:
            if conn:
                cur.close()
                conn.close()

    def insert_bulk_base_categories(self, records:list[tuple]) -> None:
        """Inserts multiple records into base_categories table
            Args:
                records:
            Returns:
                None
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
            cur = conn.cursor()
            sql_insert_query = """
                INSERT INTO 
                    base_categories (site_id, category_id, last_run, category_json)
                    VALUES (%s,%s,%s,%s)
            """
            cur.executemany(sql_insert_query, records)
            conn.commit()
        except (psycopg2.Error) as error:
            print(f"Failed to insert records into 'base_categories' table: {error}")
        finally:
            if conn:
                cur.close()
                conn.close()


    def insert_bulk_categories(self, records:list[tuple]) -> None:
        """Inserts multiple records into categories table
            Args:
                records:
            Returns:
                None
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
            cur = conn.cursor()
            sql_insert_query = """
                INSERT INTO 
                    categories (site_id, category_id, last_run, category_json)
                    VALUES (%s,%s,%s,%s)
            """
            cur.executemany(sql_insert_query, records)
            conn.commit()
        except (psycopg2.Error) as error:
            print(f"Failed to insert records into 'base_categories' table: {error}")
        finally:
            if conn:
                cur.close()
                conn.close()


    def insert_bulk_items(self, records:list[tuple]) -> None:
        """Inserts multiple records into items table
            Args:
                records:
            Returns:
                None
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
            cur = conn.cursor()
            sql_insert_query = """
                INSERT INTO 
                    items (site_id, item_id, last_run, category_id, item_json)
                    VALUES (%s,%s,%s,%s,%s)
            """
            cur.executemany(sql_insert_query, records)
            conn.commit()
        except (psycopg2.Error) as error:
            print(f"Failed to insert records into 'items' table: {error}")
        finally:
            if conn:
                cur.close()
                conn.close()


    def count_disctinct_items(self, site_id:str, category_id:str, last_run:str) -> dict:
        """Returns the number of distinct items for a given category
            Args:
                site_id:
                category_id:
                last_run:
            Returns:
                A dict
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
            cur = conn.cursor()
            postgres_read_query = """
                SELECT 
                    COUNT(*) 
                FROM (
                    SELECT 
                        DISTINCT site_id, item_id, category_id, last_run, item_json->>'order_backend' as order_backend 
                    FROM public.items 
                        WHERE site_id = %s AND category_id = %s AND last_run = %s
                ) AS temp;
            """
            cur.execute(postgres_read_query, (site_id, category_id, last_run))
            rows = cur.fetchone()
            return rows[0]
        except (psycopg2.Error) as error:
            print(f"Failed to read data from table 'items': {error}")
        finally:
            if conn:
                cur.close()
                conn.close()

    def _create_tables(self):
        """Create the necessary tables and indexes"""
        raise NotImplementedError('This function has not been implemented yet.')
