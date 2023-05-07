import frappe


class Selling:
    def __init__(self):
        self.selling = None

    def kaufland_price_list_exist(self):
        list = frappe.db.get_value('Price List', {'name': "Kaufland"}, 'name')
        if list:
            return True
        else:
            return False

    def create_price_list(self):
        price_list = frappe.get_doc({
            "doctype": "Price List",
            "name": "Kaufland",
            "price_list_name": "Kaufland",
            "currency": "EUR",
            "buying": 0,
            "selling": 1
        })
        price_list.insert()
        return price_list.name
