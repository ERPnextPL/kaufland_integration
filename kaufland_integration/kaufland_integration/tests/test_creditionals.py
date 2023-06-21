import unittest
import frappe
import frappe.defaults
from kaufland_integration.kaufland_integration.doctype.kaufland_setings.kaufland_setings import KauflandCredentials


def beforeTestsCheckIfTherIsAConfiguration():
    """
    Check if there is a configuration
    """
    creditionals = KauflandCredentials()
    if creditionals.key is None and creditionals.key != "" and creditionals.key_secret is None and creditionals.key_secret != "":
        print("* Test Failed: Keys should not be None or empty")
    else:
        print("* Test Passed: Keys are available")
