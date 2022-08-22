"""
API Client Module
"""
from __future__ import annotations
from typing import Any
import time
import uuid
import math
from requests_oauthlib import OAuth2Session
from exceptions import InvalidSite


class Client():
    """
    This class is used for identifying and authorizing users for Meli's API.
    """

    def __init__(self, client_id: str, client_secret: str, site="MLB") -> None:
        self.BASE_URL = "https://api.mercadolibre.com"
        self.auth_urls = {
            'MLA': "https://auth.mercadolibre.com.ar",  # Argentina
            'MLB': "https://auth.mercadolivre.com.br",  # Brasil
            'MCO': "https://auth.mercadolibre.com.co",  # Colombia
            'MCR': "https://auth.mercadolibre.com.cr",  # Costa Rica
            'MEC': "https://auth.mercadolibre.com.ec",  # Ecuador
            'MLC': "https://auth.mercadolibre.cl",      # Chile
            'MLM': "https://auth.mercadolibre.com.mx",  # Mexico
            'MLU': "https://auth.mercadolibre.com.uy",  # Uruguay
            'MLV': "https://auth.mercadolibre.com.ve",  # Venezuela
            'MPA': "https://auth.mercadolibre.com.pa",  # Panama
            'MPE': "https://auth.mercadolibre.com.pe",  # Peru
            'MPT': "https://auth.mercadolibre.com.pt",  # Prtugal
            'MRD': "https://auth.mercadolibre.com.do"   # Dominicana
        }
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth = None
        self.token = None
        self.client = None
        try:
            self.auth_url = self.auth_urls[site]
        except KeyError as e:
            raise InvalidSite from e

    def authorization_url(self, redirect_uri: str) -> str:
        """Returns the authorization url
            Args:
                redirect_uri:
            Returns:
                A string
        """
        self.oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri)
        state = str(uuid.uuid4())
        auth_base_url = f'{self.auth_url}/authorization'
        auth_url, state = self.oauth.authorization_url(auth_base_url, state=state)
        return auth_url

    def exchange_code(self, auth_response: str) -> dict:
        """Returns a token
            Args:
                auth_response:
            Returns:
                A dict
        """
        token_url = self.BASE_URL + "/oauth/token"
        token = self.oauth.fetch_token(
            token_url,
            include_client_id=True,
            client_secret=self.client_secret,
            authorization_response=auth_response)
        return token

    def _save_token(self, token: dict) -> None:
        self.token = token

    def set_token(self, token: dict) -> None:
        """Sets token for a new OAuth2Session
            Args:
                token:
            Returns:
                None
        """
        token_url = self.BASE_URL + '/oauth/token'
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        self.client = OAuth2Session(
            self.client_id,
            token=token,
            auto_refresh_url=token_url,
            auto_refresh_kwargs=extra,
            token_updater=self._save_token
        )
        self.token = token

    def is_valid_token(self, token: str) -> bool:
        """Verifies if the token will expires in a future point in time.
            Args:
                token:
            Returns:
                A boolean value
        """
        return token['expires_at'] > time.time()

    def me(self) -> dict[str, Any]:
        """Returns account information about the authenticated user.

        Returns:
            A dict.
        """
        return self._get('/users/me')

    def get_user(self, user_id:str) -> dict[str, Any]:
        """User account information.
        Args:
            user_id:
        Returns:
            A dict.
        """
        return self._get(f'/users/{user_id}')

    def get_user_address(self, user_id:str) -> dict[str, Any]:
        """Returns addresses registered by the user.
        Args:
            user_id:
        Returns:
            A list.
        """
        return self._get(f'/users/{user_id}/addresses')

    def get_user_accepted_payment_methods(self, user_id:str) -> list[dict[str, Any]]:
        """Returns payment methods accepted by a seller to collect its operations.
        Args:
            user_id:
        Returns:
            A list.
        """
        return self._get(f'/users/{user_id}/accepted_payment_methods')

    def get_application(self, application_id:str) -> dict[str, Any]:
        """Returns information about the application.
        Args:
            application_id:
        Returns:
            A dict.
        """
        return self._get(f'/applications/{application_id}')

    def get_user_brands(self, user_id:str):
        """This resource retrieves brands associated to an user_id.
        The official_store_id attribute identifies a store.
        Args:
            user_id:
        Returns:
            A dict.
        """
        return self._get(f'/users/{user_id}/brands')

    def get_user_classifields_promotion_packs(self, user_id):
        """Manage user promotion packs.
        Args:
            user_id:
        Returns:
            A dict.
        """
        return self._get(f'/users/{user_id}/classifieds_promotion_packs')

    def get_sites(self) -> list[dict[str, str]]:
        """Retrieves information about the sites where MercadoLibre runs.
        Returns:
            A list.
        """
        return self._get('/sites')

    def get_listing_types(self, site_id:str) -> list[dict[str, str]]:
        """Returns information about listing types.
        Args:
            site_id:
        Returns:
            A dict.
        """
        return self._get(f'/sites/{site_id}/listing_types')

    def get_listing_exposures(self, site_id:str) -> list[dict[str, str|int|bool]]:
        """Returns different exposure levels associated with all listing types in MercadoLibre.
        Args:
            site_id:
        Returns:
            A dict.
        """
        return self._get(f'/sites/{site_id}/listing_exposures')

    def get_categories(self, site_id: str) -> list[dict[str, str]]:
        """	Returns available categories in the site.
        Args:
            site_id:
        Returns:
            A list.
        """
        response = self._get(f'/sites/{site_id}/categories')
        return response

    def get_category(self, category_id:str) -> dict[str, Any]:
        """Returns information about a category.
        Args:
            category_id:
        Returns:
            A dict.
        """
        return self._get(f'/categories/{category_id}')

    def get_category_attributes(self, category_id: str):
        """Displays attributes and rules over them in order to
        describe the items that are stored in each category.
        Args:
            category_id:
        Returns:
            A dict.
        """
        return self._get(f'/categories/{category_id}/attributes')

    def get_currencies(self):
        """	Returns information about all available currencies in MercadoLibre.
        Returns:
            A list.
        """
        return self._get('/currencies')

    def get_currency(self, currency_id):
        """Returns information about available currencies in MercadoLibre by currency_id.
        Args:
            currency_id:
        Returns:
            A dict.
        """
        return self._get(f'/currencies/{currency_id}')

    def get_category_tree(self, category: dict, accumulator: list):
        """Returns a list of categories
            Args:
                category:
                accumulator:
            Returns:
                A list of dict
        """
        children_categories = category['children_categories']
        for child_category in children_categories:
            category_id = child_category["id"]
            category = self._get(f'/categories/{category_id}')
            accumulator.append(category)
            self.get_category_tree(category, accumulator)

    def get_leaf_categories(self, category: dict, accumulator: list) -> list[dict]:
        """Returns a list of leaf categories
            Args:
                category:
                accumulator:
            Returns:
                A list of dict.
        """
        if not category['children_categories']:
            accumulator.append(category)
        else:
            children_categories = category['children_categories']
            for child_category in children_categories:
                category_id = child_category["id"]
                category = self._get(f'/categories/{category_id}')
                self.get_leaf_categories(category, accumulator)

    def search_items(self, site_id: str, params: dict) -> dict:
        """Returns a dict containing the search result
            Args:
                params:
            Returns:
                A dict
        """
        return self._get(f'/sites/{site_id}/search', params=params)

    def get_items(self, site_id: str, params: dict, total: int, limit: int, quota: int) -> list[dict]:
        """Returns a list of items according query parameters.
            Args:
                params:
                total:
                limit:
            Returns:
                A list of dict
        """
        items = []
        iterations = min(math.ceil(total/limit), math.ceil(quota/limit))

        for i in range(0, iterations):
            params.update({'offset':i*limit, 'limit':limit})
            r = self._get(f'/sites/{site_id}/search', params=params)
            try:
                items.extend(r['results'])
            except KeyError:
                pass
        return items

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        url = self.BASE_URL + endpoint
        r = self.client.request(method, url, **kwargs)
        return self._parse(r)

    def _parse(self, response):
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        return r
