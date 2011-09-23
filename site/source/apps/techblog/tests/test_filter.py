from django.test import TestCase
from techblog.filter.filter import Filter, FilterItem


class TestFilter(TestCase):
    def setUp(self):
        pass

    def create_test_filter(self):
        filter = Filter()
        item = FilterItem()
        item.name = "category"
        filter.add_item(item)
        item = FilterItem()
        item.name = "tag"
        filter.add_item(item)

        return filter

    def test_load_from_session_request_only(self):
        filter = self.create_test_filter()
        request_data = {"category": "django", "tag": "db"}
        filter.load_from_request(request_data)
        self.assertEqual(filter.items[0].value, "django")
        self.assertTrue(filter.items[0].is_active)
        self.assertEqual(filter.items[1].value, "db")
        self.assertTrue(filter.items[1].is_active)

        filter = self.create_test_filter()
        request_data = {"category": "django", }
        filter.load_from_request(request_data)
        self.assertEqual(filter.items[0].value, "django")
        self.assertTrue(filter.items[0].is_active)
        self.assertEqual(filter.items[1].value, None)
        self.assertFalse(filter.items[1].is_active)

    def test_load_from_session_request_session(self):
        filter = self.create_test_filter()
        request_data = {"category": "django", }
        filter.load_from_request(request_data)
        self.assertEqual(filter.items[0].value, "django")
        self.assertTrue(filter.items[0].is_active)
        self.assertFalse(filter.items[1].is_active)

    def _test_load_from_session_request_session(self):
        filter = self.create_test_filter()
        request_data = {"all_category": None, }
        filter.load_from_request(request_data)
        self.assertEqual(filter.items[0].value, None)
        self.assertFalse(filter.items[0].is_active)
        self.assertTrue(filter.items[1].is_active)

