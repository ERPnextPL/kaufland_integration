import unittest
import frappe
import frappe.defaults
import subprocess

class TestScheduler(unittest.TestCase):
    def setUp(self):
        command = f"bench --site {frappe.local.site} scheduler enable"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    def tearDown(self):
        command = f"bench --site {frappe.local.site} scheduler disable"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    def test_checkIfschedulerIsActivate(self):
        command = f"bench --site {frappe.local.site} scheduler status"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        status_output = result.stdout.strip() 
        print(status_output)

        self.assertIn("enabled", status_output )
