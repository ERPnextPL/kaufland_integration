import unittest
import frappe
import frappe.defaults
import json
import requests
import time
import urllib.parse

from kaufland_integration.kaufland_integration.scheduler.Helper.orders import get_headers


class TestKaufland(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        pass

    def tearDown(self):
        # Clean up any resources after each test
        pass

    def test_kaufland_api_status(self):
        uri = f'https://sellerapi.kaufland.com/v2/status/ping'
        timestamp = int(time.time())
        response = requests.get(uri, headers=get_headers(uri, timestamp))
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200, "Kaufland API is not available")