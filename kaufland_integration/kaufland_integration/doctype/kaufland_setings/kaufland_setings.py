# Copyright (c) 2023, ErpTech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class KauflandCredentials:
    def __init__(self):
        self.key = self.__get_key()
        self.key_secret = self.__get_secret()

    def __get_key(self):
        return frappe.get_doc("Kaufland Setings", "api").key
    
    def __get_secret(self):
        return frappe.get_doc("Kaufland Setings", "api").secret_key



class KauflandSetings(Document):
	pass
