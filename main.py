"""
Meli-Crawler

The purpose of this script is to crawl data from Mercado Libre and save it to a database.
Such data can help in strategic decision making about seller's relevance and reputation.
"""

import os
import math
from datetime import datetime
from functools import partial
import logging
from logging.config import fileConfig
from dotenv import load_dotenv
from tqdm.contrib.concurrent import thread_map
from api import client as api_client
from db import client as db_client
from utils.utils import format_categories, format_items
from utils.utils import optimize_filters, get_filter_combinations


load_dotenv()
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
redirect_uri = os.environ.get('redirect_uri')
authorization_base_url = os.environ.get('authorization_base_url')
token_url = os.environ.get('token_url')
host = os.environ.get('host')
database = os.environ.get('database')
user = os.environ.get('user')
password = os.environ.get('password')

SITE_ID = "MLB"
API_REQUEST_QUOTA = 10000
DISTINCT_ITEMS_THRESHOLD = 0.98
TODAY = datetime.today().strftime('%Y-%m-%d')

db = db_client.Client(host, database, user, password)
api = api_client.Client(client_id, client_secret, SITE_ID)

token = db.load_token()
if api.is_valid_token(token):
    api.set_token(token)
else:
    authorization_url = api.authorization_url(redirect_uri)
    print(f'Please go to the following url and authorize access: {authorization_url}')
    authorization_response = input('Enter the full callback URL: ')
    token = api.exchange_code(authorization_response)
    api.set_token(token)
    db.save_token(token)

def crawl_categories(base_category):
    """Crawl categories"""
    leaf_categories = []
    category = api.get_category(base_category['id'])
    api.get_leaf_categories(category, leaf_categories)
    return leaf_categories

def crawl_items(category):
    """Downloads the spcified items from the API and save the data to database"""
    item_search = api.search_items(SITE_ID, {'category': category['id']})
    available_filters = item_search['available_filters']
    available_sorts = item_search['available_sorts']
    total_items = item_search['paging']['total']
    limit = item_search['paging']['limit']
    category_id = item_search['filters'][0]['values'][0]['id']
    partial_search_items = partial(api.search_items, SITE_ID)

    if total_items <= API_REQUEST_QUOTA:
        iterations = math.ceil(total_items/limit)
        params = [{'category':category_id,'offset':i*limit,'limit':limit} for i in range(iterations)]
        # searches = list(thread_map(partial_search_items, params, desc="Crawling items without filters: "))
        searches = list(map(partial_search_items, params))
        items = []
        for search in searches:
            if 'results' in search:
                items.extend(search['results'])
        formated_items = format_items(items, TODAY)
        db.insert_bulk_items(formated_items)

    else:
        optimized_filters = optimize_filters(available_filters, total_items)
        filter_combinations = get_filter_combinations(optimized_filters, available_sorts)

        for filter_combination in filter_combinations:
    
            params = {**{'category': category_id}, **filter_combination}
            item_search = api.search_items(SITE_ID, params)
            total_items = item_search['paging']['total']
            limit = item_search['paging']['limit']

            iterations = min(math.ceil(total_items/limit), math.ceil(API_REQUEST_QUOTA/limit))
            params = [{**{'category': category_id, 'offset': i*limit,
                          'limit': limit}, **filter_combination} for i in range(iterations)]
            # searches = list(thread_map(partial_search_items, params, desc="Crawling items with filters: "))
            searches = list(map(partial_search_items, params))
            items = []
            for search in searches:
                if 'results' in search:
                    items.extend(search['results'])
            
            formated_items = format_items(items, TODAY)
            db.insert_bulk_items(formated_items)

            numb_distinct_items = db.count_disctinct_items(SITE_ID, category_id[3:], TODAY)

            if numb_distinct_items >= total_items * DISTINCT_ITEMS_THRESHOLD:
                break
def main():
    """
    The flow to obtain the seller's information starts with the selection of broad base
    categories. At this point not all base categories are interesting, so a
    pre-selection is made in which only categories related to health and well-being are
    chosen. Based on a given category, it is possible to obtain subcategories that, in
    turn, are more specific and thus have a smaller number of items are more manageble
    to download. Once an item is obtained, it is possible to access the seller's
    information related to this item and its main statistics such as the number of sales
    closed in the last 60 days, number of canceled orders and other information about
    seller's reputation on Mercado Livre.
    """
    

    logger.info('Starting the crawler on %s', TODAY)

    base_categories = api.get_categories(SITE_ID)
    formated_base_categories = format_categories(base_categories, TODAY)
    db.insert_bulk_base_categories(formated_base_categories)

    logger.info('The base_categories list contains %s element(s)',
                    len(base_categories))

    # max_workers=8
    leaf_categories = thread_map(
        crawl_categories, base_categories, max_workers=4, desc='Crawling categories: ')[0]
    formated_leaf_categories = format_categories(leaf_categories, TODAY)
    db.insert_bulk_categories(formated_leaf_categories)

    logger.info('The leaf_categories list contains %s element(s)',
                len(leaf_categories))

    

    # leaf_categories = [api.get_category('MLB1384')]
    thread_map(crawl_items, leaf_categories, desc='Crawling items: ')

if __name__ == "__main__":
    fileConfig('logging_config.ini')
    logger = logging.getLogger(__name__)
    print("Welcome to Meli's Crawler.")
    main()
    print('Finished!')
