"""
This module aims to test the function in module utils
"""
from types import GeneratorType
import unittest
from utils import optimize_filters, get_filter_combinations, get_filter_generator


class TestModuleUtils(unittest.TestCase):
    """
    Test class for module utils
    """

    def test_optimized_filters(self):
        """
        Given available filters that have the same number of items,
        those filter should be removed from the list of available
        filters.
        """
        available_filters = [
            {
                "id": "official_store",
                "name": "Lojas oficiais",
                "type": "text",
                "values": [
                    {
                        "id": "all",
                        "name": "Todas las tiendas oficiales",
                        "results": 3129
                    },
                    {
                        "id": "4217",
                        "name": "Baby e Kids",
                        "results": 677
                    },
                    {
                        "id": "4650",
                        "name": "Brinkanto",
                        "results": 9
                    },
                    {
                        "id": "2138",
                        "name": "Loja MMPLACE",
                        "results": 9
                    },
                    {
                        "id": "846",
                        "name": "Planeta do Bebe",
                        "results": 76
                    },
                    {
                        "id": "1681",
                        "name": "BH Store",
                        "results": 29
                    },
                    {
                        "id": "4657",
                        "name": "Fix",
                        "results": 19
                    }
                ]
            },
            {
                "id": "discount",
                "name": "Descontos",
                "type": "number",
                "values": [
                    {
                        "id": "5-100",
                        "name": "Mais de 5% OFF",
                        "results": 337
                    },
                    {
                        "id": "10-100",
                        "name": "Mais de 10% OFF",
                        "results": 134
                    },
                    {
                        "id": "15-100",
                        "name": "Mais de 15% OFF",
                        "results": 85
                    },
                    {
                        "id": "20-100",
                        "name": "Mais de 20% OFF",
                        "results": 67
                    },
                    {
                        "id": "25-100",
                        "name": "Mais de 25% OFF",
                        "results": 58
                    },
                    {
                        "id": "30-100",
                        "name": "Mais de 30% OFF",
                        "results": 44
                    },
                    {
                        "id": "40-100",
                        "name": "Mais de 40% OFF",
                        "results": 26
                    },
                    {
                        "id": "50-100",
                        "name": "Mais de 50% OFF",
                        "results": 1
                    }
                ]
            },
            {
                "id": "accepts_mercadopago",
                "name": "Filtro por MercadoPago",
                "type": "boolean",
                "values": [
                    {
                        "id": "yes",
                        "name": "Com MercadoPago",
                        "results": 13099
                    }
                ]
            },
        ]
        expected_result = [
            {
                "id": "official_store",
                "name": "Lojas oficiais",
                "type": "text",
                "values": [
                    {
                        "id": "all",
                        "name": "Todas las tiendas oficiales",
                        "results": 3129
                    },
                    {
                        "id": "4217",
                        "name": "Baby e Kids",
                        "results": 677
                    },
                    {
                        "id": "4650",
                        "name": "Brinkanto",
                        "results": 9
                    },
                    {
                        "id": "2138",
                        "name": "Loja MMPLACE",
                        "results": 9
                    },
                    {
                        "id": "846",
                        "name": "Planeta do Bebe",
                        "results": 76
                    },
                    {
                        "id": "1681",
                        "name": "BH Store",
                        "results": 29
                    },
                    {
                        "id": "4657",
                        "name": "Fix",
                        "results": 19
                    }
                ]
            },
            {
                "id": "discount",
                "name": "Descontos",
                "type": "number",
                "values": [
                    {
                        "id": "5-100",
                        "name": "Mais de 5% OFF",
                        "results": 337
                    },
                    {
                        "id": "10-100",
                        "name": "Mais de 10% OFF",
                        "results": 134
                    },
                    {
                        "id": "15-100",
                        "name": "Mais de 15% OFF",
                        "results": 85
                    },
                    {
                        "id": "20-100",
                        "name": "Mais de 20% OFF",
                        "results": 67
                    },
                    {
                        "id": "25-100",
                        "name": "Mais de 25% OFF",
                        "results": 58
                    },
                    {
                        "id": "30-100",
                        "name": "Mais de 30% OFF",
                        "results": 44
                    },
                    {
                        "id": "40-100",
                        "name": "Mais de 40% OFF",
                        "results": 26
                    },
                    {
                        "id": "50-100",
                        "name": "Mais de 50% OFF",
                        "results": 1
                    }
                ]
            }
        ]
        total_items = 13099
        optimized_filters = optimize_filters(available_filters, total_items)
        self.assertListEqual(optimized_filters, expected_result)

    def test_get_filter_combinations(self):
        """
        Given a list of available filters, the function
        should return a list of dictionaries containing
        the combination of all filters.
        """
        optimized_filters = [
            {
                "id": "official_store",
                "name": "Lojas oficiais",
                "type": "text",
                "values": [
                    {
                        "id": "all",
                        "name": "Todas las tiendas oficiales",
                        "results": 3129
                    },
                    {
                        "id": "4217",
                        "name": "Baby e Kids",
                        "results": 677
                    },
                    {
                        "id": "4650",
                        "name": "Brinkanto",
                        "results": 9
                    },
                    {
                        "id": "2138",
                        "name": "Loja MMPLACE",
                        "results": 9
                    },
                    {
                        "id": "846",
                        "name": "Planeta do Bebe",
                        "results": 76
                    },
                    {
                        "id": "1681",
                        "name": "BH Store",
                        "results": 29
                    },
                    {
                        "id": "4657",
                        "name": "Fix",
                        "results": 19
                    }
                ]
            },
            {
                "id": "discount",
                "name": "Descontos",
                "type": "number",
                "values": [
                    {
                        "id": "5-100",
                        "name": "Mais de 5% OFF",
                        "results": 337
                    },
                    {
                        "id": "10-100",
                        "name": "Mais de 10% OFF",
                        "results": 134
                    },
                    {
                        "id": "15-100",
                        "name": "Mais de 15% OFF",
                        "results": 85
                    },
                    {
                        "id": "20-100",
                        "name": "Mais de 20% OFF",
                        "results": 67
                    },
                    {
                        "id": "25-100",
                        "name": "Mais de 25% OFF",
                        "results": 58
                    },
                    {
                        "id": "30-100",
                        "name": "Mais de 30% OFF",
                        "results": 44
                    },
                    {
                        "id": "40-100",
                        "name": "Mais de 40% OFF",
                        "results": 26
                    },
                    {
                        "id": "50-100",
                        "name": "Mais de 50% OFF",
                        "results": 1
                    }
                ]
            }
        ]
        available_sorts = [
            {
                "id": "relevance",
                "name": "Mais relevantes"
            },
            {
                "id": "price_asc",
                "name": "Menor preço"
            }
        ]
        expected_result = [
            {'official_store': 'all', 'discount': '5-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '5-100', 'sort': 'price_asc'}, 
            {'official_store': 'all', 'discount': '10-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '10-100', 'sort': 'price_asc'}, 
            {'official_store': 'all', 'discount': '15-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '15-100', 'sort': 'price_asc'}, 
            {'official_store': 'all', 'discount': '20-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '20-100', 'sort': 'price_asc'}, 
            {'official_store': 'all', 'discount': '25-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '25-100', 'sort': 'price_asc'}, 
            {'official_store': 'all', 'discount': '30-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '30-100', 'sort': 'price_asc'}, 
            {'official_store': 'all', 'discount': '40-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '40-100', 'sort': 'price_asc'}, 
            {'official_store': 'all', 'discount': '50-100', 'sort': 'relevance'}, 
            {'official_store': 'all', 'discount': '50-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '5-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '5-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '10-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '10-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '15-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '15-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '20-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '20-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '25-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '25-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '30-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '30-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '40-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '40-100', 'sort': 'price_asc'}, 
            {'official_store': '4217', 'discount': '50-100', 'sort': 'relevance'}, 
            {'official_store': '4217', 'discount': '50-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '5-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '5-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '10-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '10-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '15-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '15-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '20-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '20-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '25-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '25-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '30-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '30-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '40-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '40-100', 'sort': 'price_asc'}, 
            {'official_store': '4650', 'discount': '50-100', 'sort': 'relevance'}, 
            {'official_store': '4650', 'discount': '50-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '5-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '5-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '10-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '10-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '15-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '15-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '20-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '20-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '25-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '25-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '30-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '30-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '40-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '40-100', 'sort': 'price_asc'}, 
            {'official_store': '2138', 'discount': '50-100', 'sort': 'relevance'}, 
            {'official_store': '2138', 'discount': '50-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '5-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '5-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '10-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '10-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '15-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '15-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '20-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '20-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '25-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '25-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '30-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '30-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '40-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '40-100', 'sort': 'price_asc'}, 
            {'official_store': '846', 'discount': '50-100', 'sort': 'relevance'}, 
            {'official_store': '846', 'discount': '50-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '5-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '5-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '10-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '10-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '15-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '15-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '20-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '20-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '25-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '25-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '30-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '30-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '40-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '40-100', 'sort': 'price_asc'}, 
            {'official_store': '1681', 'discount': '50-100', 'sort': 'relevance'}, 
            {'official_store': '1681', 'discount': '50-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '5-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '5-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '10-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '10-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '15-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '15-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '20-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '20-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '25-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '25-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '30-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '30-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '40-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '40-100', 'sort': 'price_asc'}, 
            {'official_store': '4657', 'discount': '50-100', 'sort': 'relevance'}, 
            {'official_store': '4657', 'discount': '50-100', 'sort': 'price_asc'},
        ]
        filters_combinations = get_filter_combinations(optimized_filters, available_sorts)
        self.assertListEqual(filters_combinations, expected_result)

    def test_get_filter_generator(self):
        """
        Given a list of available filters, the function
        should return a list of dictionaries containing
        the combination of all filters.
        """
        optimized_filters = [
            {
                "id": "official_store",
                "name": "Lojas oficiais",
                "type": "text",
                "values": [
                    {
                        "id": "all",
                        "name": "Todas las tiendas oficiales",
                        "results": 3129
                    },
                    {
                        "id": "4217",
                        "name": "Baby e Kids",
                        "results": 677
                    },
                    {
                        "id": "4650",
                        "name": "Brinkanto",
                        "results": 9
                    },
                    {
                        "id": "2138",
                        "name": "Loja MMPLACE",
                        "results": 9
                    },
                    {
                        "id": "846",
                        "name": "Planeta do Bebe",
                        "results": 76
                    },
                    {
                        "id": "1681",
                        "name": "BH Store",
                        "results": 29
                    },
                    {
                        "id": "4657",
                        "name": "Fix",
                        "results": 19
                    }
                ]
            },
            {
                "id": "discount",
                "name": "Descontos",
                "type": "number",
                "values": [
                    {
                        "id": "5-100",
                        "name": "Mais de 5% OFF",
                        "results": 337
                    },
                    {
                        "id": "10-100",
                        "name": "Mais de 10% OFF",
                        "results": 134
                    },
                    {
                        "id": "15-100",
                        "name": "Mais de 15% OFF",
                        "results": 85
                    },
                    {
                        "id": "20-100",
                        "name": "Mais de 20% OFF",
                        "results": 67
                    },
                    {
                        "id": "25-100",
                        "name": "Mais de 25% OFF",
                        "results": 58
                    },
                    {
                        "id": "30-100",
                        "name": "Mais de 30% OFF",
                        "results": 44
                    },
                    {
                        "id": "40-100",
                        "name": "Mais de 40% OFF",
                        "results": 26
                    },
                    {
                        "id": "50-100",
                        "name": "Mais de 50% OFF",
                        "results": 1
                    }
                ]
            }
        ]
        available_sorts = [
            {
                "id": "relevance",
                "name": "Mais relevantes"
            },
            {
                "id": "price_asc",
                "name": "Menor preço"
            }
        ]
        expected_result = [
            {'official_store': 'all'},
            {'official_store': '4217'},
            {'official_store': '4650'},
            {'official_store': '2138'},
            {'official_store': '846'},
            {'official_store': '1681'},
            {'official_store': '4657'},
            {'discount': '5-100'},
            {'discount': '10-100'},
            {'discount': '15-100'},
            {'discount': '20-100'},
            {'discount': '25-100'},
            {'discount': '30-100'},
            {'discount': '40-100'},
            {'discount': '50-100'},
            {'sort': 'relevance'},
            {'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '5-100'},
            {'official_store': 'all', 'discount': '10-100'},
            {'official_store': 'all', 'discount': '15-100'},
            {'official_store': 'all', 'discount': '20-100'},
            {'official_store': 'all', 'discount': '25-100'},
            {'official_store': 'all', 'discount': '30-100'},
            {'official_store': 'all', 'discount': '40-100'},
            {'official_store': 'all', 'discount': '50-100'},
            {'official_store': '4217', 'discount': '5-100'},
            {'official_store': '4217', 'discount': '10-100'},
            {'official_store': '4217', 'discount': '15-100'},
            {'official_store': '4217', 'discount': '20-100'},
            {'official_store': '4217', 'discount': '25-100'},
            {'official_store': '4217', 'discount': '30-100'},
            {'official_store': '4217', 'discount': '40-100'},
            {'official_store': '4217', 'discount': '50-100'},
            {'official_store': '4650', 'discount': '5-100'},
            {'official_store': '4650', 'discount': '10-100'},
            {'official_store': '4650', 'discount': '15-100'},
            {'official_store': '4650', 'discount': '20-100'},
            {'official_store': '4650', 'discount': '25-100'},
            {'official_store': '4650', 'discount': '30-100'},
            {'official_store': '4650', 'discount': '40-100'},
            {'official_store': '4650', 'discount': '50-100'},
            {'official_store': '2138', 'discount': '5-100'},
            {'official_store': '2138', 'discount': '10-100'},
            {'official_store': '2138', 'discount': '15-100'},
            {'official_store': '2138', 'discount': '20-100'},
            {'official_store': '2138', 'discount': '25-100'},
            {'official_store': '2138', 'discount': '30-100'},
            {'official_store': '2138', 'discount': '40-100'},
            {'official_store': '2138', 'discount': '50-100'},
            {'official_store': '846', 'discount': '5-100'},
            {'official_store': '846', 'discount': '10-100'},
            {'official_store': '846', 'discount': '15-100'},
            {'official_store': '846', 'discount': '20-100'},
            {'official_store': '846', 'discount': '25-100'},
            {'official_store': '846', 'discount': '30-100'},
            {'official_store': '846', 'discount': '40-100'},
            {'official_store': '846', 'discount': '50-100'},
            {'official_store': '1681', 'discount': '5-100'},
            {'official_store': '1681', 'discount': '10-100'},
            {'official_store': '1681', 'discount': '15-100'},
            {'official_store': '1681', 'discount': '20-100'},
            {'official_store': '1681', 'discount': '25-100'},
            {'official_store': '1681', 'discount': '30-100'},
            {'official_store': '1681', 'discount': '40-100'},
            {'official_store': '1681', 'discount': '50-100'},
            {'official_store': '4657', 'discount': '5-100'},
            {'official_store': '4657', 'discount': '10-100'},
            {'official_store': '4657', 'discount': '15-100'},
            {'official_store': '4657', 'discount': '20-100'},
            {'official_store': '4657', 'discount': '25-100'},
            {'official_store': '4657', 'discount': '30-100'},
            {'official_store': '4657', 'discount': '40-100'},
            {'official_store': '4657', 'discount': '50-100'},
            {'official_store': 'all', 'sort': 'relevance'},
            {'official_store': 'all', 'sort': 'price_asc'},
            {'official_store': '4217', 'sort': 'relevance'},
            {'official_store': '4217', 'sort': 'price_asc'},
            {'official_store': '4650', 'sort': 'relevance'},
            {'official_store': '4650', 'sort': 'price_asc'},
            {'official_store': '2138', 'sort': 'relevance'},
            {'official_store': '2138', 'sort': 'price_asc'},
            {'official_store': '846', 'sort': 'relevance'},
            {'official_store': '846', 'sort': 'price_asc'},
            {'official_store': '1681', 'sort': 'relevance'},
            {'official_store': '1681', 'sort': 'price_asc'},
            {'official_store': '4657', 'sort': 'relevance'},
            {'official_store': '4657', 'sort': 'price_asc'},
            {'discount': '5-100', 'sort': 'relevance'},
            {'discount': '5-100', 'sort': 'price_asc'},
            {'discount': '10-100', 'sort': 'relevance'},
            {'discount': '10-100', 'sort': 'price_asc'},
            {'discount': '15-100', 'sort': 'relevance'},
            {'discount': '15-100', 'sort': 'price_asc'},
            {'discount': '20-100', 'sort': 'relevance'},
            {'discount': '20-100', 'sort': 'price_asc'},
            {'discount': '25-100', 'sort': 'relevance'},
            {'discount': '25-100', 'sort': 'price_asc'},
            {'discount': '30-100', 'sort': 'relevance'},
            {'discount': '30-100', 'sort': 'price_asc'},
            {'discount': '40-100', 'sort': 'relevance'},
            {'discount': '40-100', 'sort': 'price_asc'},
            {'discount': '50-100', 'sort': 'relevance'},
            {'discount': '50-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '5-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '5-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '10-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '10-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '15-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '15-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '20-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '20-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '25-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '25-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '30-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '30-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '40-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '40-100', 'sort': 'price_asc'},
            {'official_store': 'all', 'discount': '50-100', 'sort': 'relevance'},
            {'official_store': 'all', 'discount': '50-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '5-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '5-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '10-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '10-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '15-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '15-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '20-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '20-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '25-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '25-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '30-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '30-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '40-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '40-100', 'sort': 'price_asc'},
            {'official_store': '4217', 'discount': '50-100', 'sort': 'relevance'},
            {'official_store': '4217', 'discount': '50-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '5-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '5-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '10-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '10-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '15-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '15-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '20-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '20-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '25-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '25-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '30-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '30-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '40-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '40-100', 'sort': 'price_asc'},
            {'official_store': '4650', 'discount': '50-100', 'sort': 'relevance'},
            {'official_store': '4650', 'discount': '50-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '5-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '5-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '10-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '10-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '15-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '15-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '20-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '20-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '25-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '25-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '30-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '30-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '40-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '40-100', 'sort': 'price_asc'},
            {'official_store': '2138', 'discount': '50-100', 'sort': 'relevance'},
            {'official_store': '2138', 'discount': '50-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '5-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '5-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '10-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '10-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '15-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '15-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '20-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '20-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '25-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '25-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '30-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '30-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '40-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '40-100', 'sort': 'price_asc'},
            {'official_store': '846', 'discount': '50-100', 'sort': 'relevance'},
            {'official_store': '846', 'discount': '50-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '5-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '5-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '10-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '10-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '15-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '15-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '20-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '20-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '25-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '25-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '30-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '30-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '40-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '40-100', 'sort': 'price_asc'},
            {'official_store': '1681', 'discount': '50-100', 'sort': 'relevance'},
            {'official_store': '1681', 'discount': '50-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '5-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '5-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '10-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '10-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '15-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '15-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '20-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '20-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '25-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '25-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '30-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '30-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '40-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '40-100', 'sort': 'price_asc'},
            {'official_store': '4657', 'discount': '50-100', 'sort': 'relevance'},
            {'official_store': '4657', 'discount': '50-100', 'sort': 'price_asc'},
        ]
        filters_combinations = get_filter_generator(optimized_filters, available_sorts)
        self.assertIsInstance(filters_combinations, GeneratorType)
        self.assertListEqual(list(filters_combinations), expected_result)

unittest.main(argv=[''], verbosity=2, exit=False)
