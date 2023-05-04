import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job


class Products:
    def __init__(self):
        self.products = None

    def product_exist(self,product, log):
        ean = product["eans"]
        customer = frappe.db.get_value('Item', {'item_code': ean[0]}, 'name')
        if customer:
            return True
        else:
            add_comment_to_job(
                log, f"Product with ean: '{ean[0]}' does not exist in ErpNext. Adding new Item")
            return False

    def __brand_exist(self,name):
        brand = frappe.db.get_value('Brand', {'name': name}, 'name')
        if brand:
            return True
        else:
            return False

    def __create_brand(self,name):
        brand = frappe.get_doc({
            "doctype": "Brand",
            "brand": name
        })
        brand.insert()


    def create_product(self, item, log):
        eans = item["eans"]
        
        if not self.__brand_exist(item["manufacturer"]):
           self.__create_brand(item["manufacturer"])
        
        product = frappe.get_doc({
            "doctype": "Item",
            "item_code": eans[0],
            "item_group": "Produkty",
            "item_name": item["title"],
            "brand": item["manufacturer"],
            "stock_uom": "szt.",
            "is_purchase_item": 1,
            "purchase_uom": "szt.",
            "sales_uom": "szt.",
            "is_sales_item": 1,
            "image": item["main_picture"]
        })
        product.insert()

