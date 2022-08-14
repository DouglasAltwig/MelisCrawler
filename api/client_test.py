import os
import unittest
from urllib.parse import urlparse
from urllib.parse import parse_qsl
from dotenv import load_dotenv
from client import Client


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        load_dotenv()
        client_id = os.environ.get('client_id')
        client_secret = os.environ.get('client_secret')
        redirect_uri = os.environ.get('redirect_uri')
        
        cls.api = Client(client_id, client_secret, 'MLB')
        authorization_url = cls.api.authorization_url(redirect_uri)
        print(f'Please go to the following url and authorize access: {authorization_url}')
        authorization_response = input('Enter the full callback URL: ')
        token = cls.api.exchange_code(authorization_response)
        cls.api.set_token(token)

    def setUp(self):
        self.client_id = os.environ.get('client_id')
        self.client_secret = os.environ.get('client_secret')
        self.redirect_uri = os.environ.get('redirect_uri')

    def test_authorization_url(self):
        authorization_url = TestClient.api.authorization_url(self.redirect_uri)
        params = {
            'response_type':'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        query_params = dict(parse_qsl(urlparse(authorization_url).query))
        self.assertDictContainsSubset(params, query_params)

    def test_me(self):
        me = TestClient.api.me()
        expected = ['id', 'nickname', 'registration_date', 'first_name', 'last_name']
        self.assertGreaterEqual(list(me.keys()), expected)

    def test_get_sites(self):
        expected_sites = [
            {'default_currency_id': 'USD', 'id': 'MSV', 'name': 'El Salvador'}, 
            {'default_currency_id': 'CLP', 'id': 'MLC', 'name': 'Chile'}, 
            {'default_currency_id': 'PEN', 'id': 'MPE', 'name': 'Perú'}, 
            {'default_currency_id': 'MXN', 'id': 'MLM', 'name': 'Mexico'}, 
            {'default_currency_id': 'VES', 'id': 'MLV', 'name': 'Venezuela'}, 
            {'default_currency_id': 'HNL', 'id': 'MHN', 'name': 'Honduras'}, 
            {'default_currency_id': 'CUP', 'id': 'MCU', 'name': 'Cuba'}, 
            {'default_currency_id': 'BRL', 'id': 'MLB', 'name': 'Brasil'}, 
            {'default_currency_id': 'USD', 'id': 'MEC', 'name': 'Ecuador'}, 
            {'default_currency_id': 'COP', 'id': 'MCO', 'name': 'Colombia'}, 
            {'default_currency_id': 'ARS', 'id': 'MLA', 'name': 'Argentina'}, 
            {'default_currency_id': 'PAB', 'id': 'MPA', 'name': 'Panamá'}, 
            {'default_currency_id': 'GTQ', 'id': 'MGT', 'name': 'Guatemala'}, 
            {'default_currency_id': 'DOP', 'id': 'MRD', 'name': 'Dominicana'}, 
            {'default_currency_id': 'PYG', 'id': 'MPY', 'name': 'Paraguay'}, 
            {'default_currency_id': 'NIO', 'id': 'MNI', 'name': 'Nicaragua'}, 
            {'default_currency_id': 'UYU', 'id': 'MLU', 'name': 'Uruguay'}, 
            {'default_currency_id': 'BOB', 'id': 'MBO', 'name': 'Bolivia'}, 
            {'default_currency_id': 'CRC', 'id': 'MCR', 'name': 'Costa Rica'}]
        sites = TestClient.api.get_sites()
        self.assertListEqual(
            sorted(sites, key=lambda d: d['name']),
            sorted(expected_sites, key=lambda d: d['name']))

    def test_get_currencies(self):
        expected_currencies = [
            {'id': 'ARS', 'symbol': '$', 'description': 'Peso argentino', 'decimal_places': 2}, 
            {'id': 'BOB', 'symbol': 'Bs', 'description': 'Boliviano', 'decimal_places': 2}, 
            {'id': 'BRL', 'symbol': 'R$', 'description': 'Real', 'decimal_places': 2}, 
            {'id': 'CLF', 'symbol': 'UF', 'description': 'Unidad de Fomento', 'decimal_places': 2}, 
            {'id': 'CLP', 'symbol': '$', 'description': 'Peso Chileno', 'decimal_places': 0}, 
            {'id': 'COP', 'symbol': '$', 'description': 'Peso colombiano', 'decimal_places': 0}, 
            {'id': 'CRC', 'symbol': '₡', 'description': 'Colones', 'decimal_places': 2}, 
            {'id': 'CUC', 'symbol': 'CUC', 'description': 'Peso Cubano Convertible', 'decimal_places': 2}, 
            {'id': 'CUP', 'symbol': '$', 'description': 'Peso Cubano', 'decimal_places': 2}, 
            {'id': 'DOP', 'symbol': '$', 'description': 'Peso Dominicano', 'decimal_places': 2}, 
            {'id': 'EUR', 'symbol': '€', 'description': 'Euro', 'decimal_places': 2}, 
            {'id': 'GTQ', 'symbol': 'Q', 'description': 'Quetzal Guatemalteco', 'decimal_places': 2}, 
            {'id': 'HNL', 'symbol': 'L', 'description': 'Lempira', 'decimal_places': 0}, 
            {'id': 'MXN', 'symbol': '$', 'description': 'Peso Mexicano', 'decimal_places': 2}, 
            {'id': 'NIO', 'symbol': 'C$', 'description': 'Córdoba', 'decimal_places': 0}, 
            {'id': 'PAB', 'symbol': 'B/.', 'description': 'Balboa', 'decimal_places': 2}, 
            {'id': 'PEN', 'symbol': 'S/', 'description': 'Soles', 'decimal_places': 2}, 
            {'id': 'PYG', 'symbol': '₲', 'description': 'Guaraní', 'decimal_places': 0}, 
            {'id': 'USD', 'symbol': 'U$S', 'description': 'Dólar', 'decimal_places': 2}, 
            {'id': 'UYU', 'symbol': '$', 'description': 'Peso Uruguayo', 'decimal_places': 2}, 
            {'id': 'VEF', 'symbol': 'Bs.', 'description': 'Bolivar fuerte', 'decimal_places': 2}, 
            {'id': 'VES', 'symbol': 'Bs.', 'description': 'Bolivar Soberano', 'decimal_places': 2}]
        currencies = TestClient.api.get_currencies()
        self.assertListEqual(currencies, expected_currencies)

    def test_get_currency(self):
        expected_currency = {
            'id': 'BRL', 
            'symbol': 'R$', 
            'description': 'Real', 
            'decimal_places': 2}
        currency = TestClient.api.get_currency('BRL')
        self.assertDictEqual(currency, expected_currency)

    def test_get_categories_instance_type(self):
        self.assertIsInstance(TestClient.api.get_categories('MLB'), list)

    def test_get_categories(self):
        expected_categories = [
            {'id': 'MLB5672', 'name': 'Acessórios para Veículos'}, 
            {'id': 'MLB271599', 'name': 'Agro'}, 
            {'id': 'MLB1403', 'name': 'Alimentos e Bebidas'}, 
            {'id': 'MLB1071', 'name': 'Animais'}, 
            {'id': 'MLB1367', 'name': 'Antiguidades e Coleções'}, 
            {'id': 'MLB1368', 'name': 'Arte, Papelaria e Armarinho'}, 
            {'id': 'MLB1384', 'name': 'Bebês'}, 
            {'id': 'MLB1246', 'name': 'Beleza e Cuidado Pessoal'}, 
            {'id': 'MLB1132', 'name': 'Brinquedos e Hobbies'}, 
            {'id': 'MLB1430', 'name': 'Calçados, Roupas e Bolsas'}, 
            {'id': 'MLB1039', 'name': 'Câmeras e Acessórios'}, 
            {'id': 'MLB1743', 'name': 'Carros, Motos e Outros'}, 
            {'id': 'MLB1574', 'name': 'Casa, Móveis e Decoração'}, 
            {'id': 'MLB1051', 'name': 'Celulares e Telefones'}, 
            {'id': 'MLB1500', 'name': 'Construção'}, 
            {'id': 'MLB5726', 'name': 'Eletrodomésticos'}, 
            {'id': 'MLB1000', 'name': 'Eletrônicos, Áudio e Vídeo'}, 
            {'id': 'MLB1276', 'name': 'Esportes e Fitness'}, 
            {'id': 'MLB263532', 'name': 'Ferramentas'}, 
            {'id': 'MLB12404', 'name': 'Festas e Lembrancinhas'}, 
            {'id': 'MLB1144', 'name': 'Games'}, 
            {'id': 'MLB1459', 'name': 'Imóveis'}, 
            {'id': 'MLB1499', 'name': 'Indústria e Comércio'}, 
            {'id': 'MLB1648', 'name': 'Informática'}, 
            {'id': 'MLB218519', 'name': 'Ingressos'}, 
            {'id': 'MLB1182', 'name': 'Instrumentos Musicais'}, 
            {'id': 'MLB3937', 'name': 'Joias e Relógios'}, 
            {'id': 'MLB1196', 'name': 'Livros, Revistas e Comics'}, 
            {'id': 'MLB1168', 'name': 'Música, Filmes e Seriados'}, 
            {'id': 'MLB264586', 'name': 'Saúde'}, 
            {'id': 'MLB1540', 'name': 'Serviços'}, 
            {'id': 'MLB1953', 'name': 'Mais Categorias'}
        ]
        categories = TestClient.api.get_categories("MLB")
        self.assertListEqual(categories, expected_categories)

    def test_get_categories_from_unknown_site(self):
        unknown_site_id = 'MLX'
        response = TestClient.api.get_categories(unknown_site_id)
        not_found = {'message': 'Categories not found for this site', 'error': 'not_found', 'status': 404, 'cause': []}
        self.assertDictEqual(response, not_found)

    def test_get_category(self):
        category = TestClient.api.get_category('MLB5360')
        self.assertEqual(category['id'], 'MLB5360')

    def test_get_category_name(self):
        category = TestClient.api.get_category('MLB5360')
        self.assertEqual(category['name'], 'Alimentação e Amamentação')

    def test_leaf_categories_no_children(self):
        leaf_categories = []
        category = TestClient.api.get_category('MLB5360')
        TestClient.api.get_leaf_categories(category, leaf_categories)
        [self.assertListEqual(leaf_category['children_categories'], [])
         for leaf_category in leaf_categories]

    def test_search_items_type(self):
        item_search = TestClient.api.search_items('MLB', {'category_id': 'MLB5360'})
        self.assertIsInstance(item_search, dict)

    def test_search_items_contains_result(self):
        item_search = TestClient.api.search_items('MLB', {'category': 'MLB5360'})
        self.assertIn('results', item_search.keys())

    def test_search_items_result_len(self):
        item_search = TestClient.api.search_items('MLB', {'category': 'MLB5360'})
        self.assertGreater(len(item_search['results']), 0)

    def test_search_items_from_unknown_site(self):
        unknown_site = 'MLX'
        response = TestClient.api.search_items(unknown_site, {'category': 'MLB5360'})
        not_found = {'message': 'This host is not serving site MLX', 'error': 'bad_request', 'status': 400, 'cause': []}
        self.assertDictEqual(response, not_found)

    def test_search_items_unknown_category(self):
        unknown_category = 'MLBUNKNOWN'
        item_search = TestClient.api.search_items('MLB', {'category': unknown_category})
        self.assertCountEqual(item_search['results'], [])

    def test_search_items_paging_info(self):
        item_search = TestClient.api.search_items('MLB', {'category_id': 'MLB5360'})
        self.assertIn('paging', item_search)
        self.assertIn('total', item_search['paging'])
        self.assertIn('offset', item_search['paging'])
        self.assertIn('limit', item_search['paging'])

    def test_get_items_under_10000(self):
        # MLB264021 -> Bombinhas de Tirar Leite
        item_search = TestClient.api.search_items('MLB', {'category': 'MLB264021'})
        total = item_search['paging']['total']  # 7287
        category_id = item_search['filters'][0]['values'][0]['id']
        limit = item_search['paging']['limit']
        quota = 10000
        items = TestClient.api.get_items('MLB', {'category': category_id}, total, limit, quota)
        self.assertAlmostEqual(total, len(items), None, '', total*0.05)

    def test_get_items_over_10000(self):
        # MLB40554 -> Cadeiras de Alimentação
        item_search = TestClient.api.search_items('MLB', {'category': 'MLB40554'})
        total = item_search['paging']['total']  # 13087
        category_id = item_search['filters'][0]['values'][0]['id']
        limit = item_search['paging']['limit']
        quota = 10000
        items = TestClient.api.get_items('MLB', {'category': category_id}, total, limit, quota)
        self.assertAlmostEqual(total, len(items), None, '', total*0.05)

    def test_get_category_attributes_contains_brand(self):
        attributes = TestClient.api.get_category_attributes('MLB40554')
        contains_brand = any(('id', 'BRAND') in attribute.items() for attribute in attributes )
        self.assertTrue(contains_brand)

    def test_get_category_attributes_contains_values(self):
        attributes = TestClient.api.get_category_attributes('MLB40554')
        contains_values = any('values' in attribute for attribute in attributes )
        self.assertTrue(contains_values)

    def test_refresh_token(self):
        pass
    
unittest.main(argv=[''], verbosity=2, exit=False)