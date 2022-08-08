import unittest


class TestClient(unittest.TestCase):

    def setUp(self):
        self.categories = get_base_categories('MLB')
        self.unknown_site_id = get_base_categories('UNKNOWN_CATEGORY_ID')
        self.msg_unknown_site_id = {
            'message': 'Categories not found for this site', 'error': 'not_found', 'status': 404, 'cause': []}
        self.category = get_category("MLB5360")
        self.search_result_known_category = search_items(
            {'category': 'MLB5360'})
        self.search_result_unknown_category = search_items(
            {'category': 'UNKNOWN_CATEGORY_ID'})

    def test_get_base_categories_returns_list(self):
        self.assertIsInstance(self.categories, list)

    def test_get_base_categories_returns_no_empty_list(self):
        self.assertGreater(len(self.categories), 0)

    def test_get_base_categories_unknown_site_id(self):
        self.assertDictEqual(self.unknown_site_id, self.msg_unknown_site_id)

    def test_get_category_id(self):
        self.assertEqual(self.category['id'], 'MLB5360')

    def test_get_category_name(self):
        self.assertEqual(self.category['name'], 'Alimentação e Amamentação')

    def test_leaf_categories_have_no_children(self):
        leaf_categories = []
        get_leaf_categories(self.category, leaf_categories)
        [self.assertListEqual(leaf_category['children_categories'], [])
         for leaf_category in leaf_categories]

    def test_search_items_type(self):
        self.assertIsInstance(self.search_result_known_category, dict)

    def test_search_items_contains_result(self):
        self.assertIn('results', self.search_result_known_category.keys())

    def test_search_items_known_category(self):
        self.assertGreater(
            len(self.search_result_known_category['results']), 0)

    def test_search_items_paging_info(self):
        self.assertIn('paging', self.search_result_known_category)
        self.assertIn('total', self.search_result_known_category['paging'])
        self.assertIn('offset', self.search_result_known_category['paging'])
        self.assertIn('limit', self.search_result_known_category['paging'])

    def test_search_items_unknown_result(self):
        self.assertIn('results', self.search_result_unknown_category.keys())

    def test_search_items_unknown_category(self):
        self.assertCountEqual(
            self.search_result_unknown_category['results'], [])

    def test_get_items_under_10000(self):
        # Bombinhas de Tirar Leite
        search_result = search_items({'category': 'MLB264021'})
        total = search_result['paging']['total']  # 7287
        category_id = search_result['filters'][0]['values'][0]['id']
        limit = search_result['paging']['limit']

        items = get_items({'category': category_id}, total, limit)
        self.assertEqual(total, len(items))

    def test_get_items_over_10000(self):
        # Cadeiras de Alimentação
        search_result = search_items({'category': 'MLB40554'})
        total = search_result['paging']['total']  # 13087
        category_id = search_result['filters'][0]['values'][0]['id']
        limit = search_result['paging']['limit']

        items = get_items({'category': category_id}, total, limit)
        self.assertEqual(10000, len(items))



unittest.main(argv=[''], verbosity=2, exit=False)