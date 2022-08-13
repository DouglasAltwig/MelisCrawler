"""
API Client Module
"""
from __future__ import annotations
from typing import Any
import time
import uuid
import math
import json
import logging
from logging.config import fileConfig
from urllib.parse import urlencode, parse_qsl, urlsplit
import requests
from requests.structures import CaseInsensitiveDict

from exceptions import InvalidSite
from decorators import valid_token

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)


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
        self.access_token = None
        self._refresh_token = None
        self.user_id = None
        self.expires_in = None
        self.expires_at = None
        try:
            self.auth_url = self.auth_urls[site]
        except KeyError as e:
            raise InvalidSite from e

    def authorization_url(self, redirect_uri: str) -> str:
        """URL"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'state': str(uuid.uuid4())
        }
        encoded_params = urlencode(params)
        url = f'{self.auth_url}/authorization?{encoded_params}'
        return url

    def urlparse(self, url):
        """Parse url"""
        params = dict(parse_qsl(urlsplit(url).query))
        return params

    def exchange_code(self, redirect_uri, code):
        """Exchange code"""
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        return self._token(self._post('/oauth/token', params=params, headers=headers))

    def refresh_token(self):
        """Refresh token"""
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token
        }
        return self._token(self._post('/oauth/token', params=params))

    def set_token(self, token):
        """Set token"""
        if isinstance(token, dict):
            self.access_token = token.get('access_token', None)
            self._refresh_token = token.get('refresh_token', None)
            self.user_id = token.get('user_id', None)
            self.expires_in = token.get('expires_in', None)
            self.expires_at = token.get('expires_at', None)
        else:
            self.access_token = token

    @property
    def is_valid_token(self):
        """Valid token"""
        if self.expires_at:
            return self.expires_at > time.time()
        return None

    @valid_token
    def me(self) -> dict[str, Any]:
        """Returns account information about the authenticated user.

        Returns:
            A dict.
        """
        return self._get('/users/me')

    @valid_token
    def get_user(self, user_id:str) -> dict[str, Any]:
        """User account information.
        Args:
            user_id:
        Returns:
            A dict.
        """
        return self._get(f'/users/{user_id}')

    @valid_token
    def get_user_address(self, user_id:str) -> dict[str, Any]:
        """Returns addresses registered by the user.
        Args:
            user_id:
        Returns:
            A list.
        """
        return self._get(f'/users/{user_id}/addresses')

    @valid_token
    def get_user_accepted_payment_methods(self, user_id:str) -> list[dict[str, Any]]:
        """Returns payment methods accepted by a seller to collect its operations.
        Args:
            user_id:
        Returns:
            A list.
        """
        return self._get(f'/users/{user_id}/accepted_payment_methods')

    @valid_token
    def get_application(self, application_id:str) -> dict[str, Any]:
        """Returns information about the application.
        Args:
            application_id:
        Returns:
            A dict.
        """
        return self._get(f'/applications/{application_id}')

    @valid_token
    def get_user_brands(self, user_id:str):
        """This resource retrieves brands associated to an user_id.
        The official_store_id attribute identifies a store.
        Args:
            user_id:
        Returns:
            A dict.
        """
        return self._get(f'/users/{user_id}/brands')

    @valid_token
    def get_user_classifields_promotion_packs(self, user_id):
        """Manage user promotion packs.
        Args:
            user_id:
        Returns:
            A dict.
        """
        return self._get(f'/users/{user_id}/classifieds_promotion_packs')

    @valid_token
    def get_sites(self) -> list[dict[str, str]]:
        """Retrieves information about the sites where MercadoLibre runs.
        Returns:
            A list.
        """
        return self._get('/sites')

    @valid_token
    def get_listing_types(self, site_id:str) -> list[dict[str, str]]:
        """Returns information about listing types.
        Args:
            site_id:
        Returns:
            A dict.
        """
        return self._get(f'/sites/{site_id}/listing_types')

    @valid_token
    def get_listing_exposures(self, site_id:str) -> list[dict[str, str|int|bool]]:
        """Returns different exposure levels associated with all listing types in MercadoLibre.
        Args:
            site_id:
        Returns:
            A dict.
        """
        return self._get(f'/sites/{site_id}/listing_exposures')

    @valid_token
    def get_categories(self, site_id: str) -> list[dict[str, str]]:
        """	Returns available categories in the site.
        Args:
            site_id:
        Returns:
            A list.
        """
        response = self._get(f'/sites/{site_id}/categories')
        return response

    @valid_token
    def get_category(self, category_id:str) -> dict[str, Any]:
        """Returns information about a category.
        Args:
            category_id:
        Returns:
            A dict.
        """
        return self._get(f'/categories/{category_id}')

    @valid_token
    def get_category_attributes(self, category_id: str):
        """Displays attributes and rules over them in order to
        describe the items that are stored in each category.
        Args:
            category_id:
        Returns:
            A dict.
        """
        return self._get(f'/categories/{category_id}/attributes')

    @valid_token
    def get_currencies(self):
        """	Returns information about all available currencies in MercadoLibre.
        Returns:
            A list.
        """
        return self._get('/currencies')

    @valid_token
    def get_currency(self, currency_id):
        """Returns information about available currencies in MercadoLibre by currency_id.
        Args:
            currency_id:
        Returns:
            A dict.
        """
        return self._get(f'/currencies/{currency_id}')

    @valid_token
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

    @valid_token
    def search_items(self, site_id: str, params: dict) -> dict:
        """Returns a dict containing the search result
            Args:
                params:
            Returns:
                A dict
        """
        return self._get(f'/sites/{site_id}/search', params=params)

    @valid_token
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
                logger.error('url: %s, response: %s',
                             f'/sites/{site_id}/search', json.dumps(params))
        return items

    def _token(self, response):
        if 'expires_in' in response:
            expires_in = response['expires_in']
            expires_at = time.time() + int(expires_in)
            response['expires_at'] = expires_at
            self.expires_at = expires_at
        return response

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)

    def _request(self, method, endpoint, params=None, **kwargs):
        headers = kwargs.pop('headers', {})
        if self.access_token:
            _headers = {
                'accept': 'application/json',
                'authorization': f'Bearer {self.access_token}'
            }
            headers.update(_headers)
        url = self.BASE_URL + endpoint
        r = requests.request(method, url, params=params, headers=headers, **kwargs)
        return self._parse(r)

    def _parse(self, response):
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        return r
