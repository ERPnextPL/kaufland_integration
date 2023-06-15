import json
import requests
import time
import hmac
import hashlib
import urllib.parse
import frappe
from datetime import datetime
from kaufland_integration.kaufland_integration.doctype.kaufland_setings.kaufland_setings import KauflandCredentials
from kaufland_integration.kaufland_integration.scheduler.Helper.exchange_rates import ExchangeRates
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.selling import Selling
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.products import Products
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.payment import Payment
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.customer import Customer
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job, set_job_async


def get_headers(url: str, timestamp: int):
    creditionals = KauflandCredentials()
    return {
        'Accept': 'application/json',
        'Shop-Client-Key': creditionals.key,
        'Shop-Timestamp': str(timestamp),
        'Shop-Signature': sign_request('GET', url, '', timestamp, creditionals.key_secret)
    }


def sign_request(method, uri, body, timestamp, secret_key):
    plain_text = "\n".join([method, uri, body, str(timestamp)])
    digest_maker = hmac.new(secret_key.encode(), None, hashlib.sha256)
    digest_maker.update(plain_text.encode())
    return digest_maker.hexdigest()

#################################################################################################


def get_orders_form_kaufland(dateFrom: str, log):

    params = { 'fulfillment_type': 'fulfilled_by_merchant',
              'ts_created_from_iso': dateFrom,'limit':100}
    uri = f'https://sellerapi.kaufland.com/v2/orders?{urllib.parse.urlencode(params)}'
    timestamp = int(time.time())
    try:
        response = requests.get(uri, headers=get_headers(uri, timestamp))
        response.raise_for_status()
        data = json.loads(response.content.decode("utf-8"))
        if data != None:
            try:
                orders = [id_order["id_order"] for id_order in data["data"]]
                return orders
            except KeyError as e:
                add_comment_to_job(log, f"Error: {e}")
        else:
            return None
    except requests.exceptions.HTTPError as e:
        add_comment_to_job(log, f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        add_comment_to_job(log, f"Request error: {e}")

#################################################################################################


def get_order_form_kaufland_by_id(id_order: str, log):
    params = {'embedded': 'order_invoices'}
    uri = f'https://sellerapi.kaufland.com/v2/orders/{id_order}?{urllib.parse.urlencode(params)}'
    timestamp = int(time.time())
    response = requests.get(uri, headers=get_headers(uri, timestamp))
    data = json.loads(response.content.decode("utf-8"))
    if data != None:
        add_comment_to_job(log, f"Order[{id_order}]: {str(data)}")
        if not order_exist(id_order, log):
            set_job_async(jobName=f"ErpNext.CreateNewSalesOrder",
                          methodPath=f"kaufland_integration.kaufland_integration.scheduler.Helper.orders.create_order_from_kaufland_data", queue="default", data=data["data"], log=log)
    else:
        add_comment_to_job(log, f"No data for order {id_order}")

#################################################################################################


def create_order_from_kaufland_data(data, log):
    buyer = data["buyer"]
    id_order = data["id_order"]
    date = data["ts_created_iso"]
    datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    po_date = datetime_obj.strftime("%Y-%m-%d")

    # price list section
    selling = Selling()

    # customer section
    customer = Customer()
    if not customer.customer_exist(buyer["email"], log):
        customer_name = customer.create_customer(data, log)
    else:
        customer_name = customer.get_customer_name(buyer["email"])
        
    territory = customer.get_customer_territory(customer_name)
    
    # product section
    products = Products()
    sales_order_items = []
    order_items = data["order_units"]
    for item in order_items:
        product = item["product"]
        if not products.product_exist(product, log):
            products.create_product(product, log)
        sales_order_items.append(products.get_sales_roder_item_structure(item, len(sales_order_items)))
    
    # first unit
    status_order = order_items[0]["status"]

    # Payment terms
    payment = Payment()

    # Exchange Rates
    exchange_rates = ExchangeRates()
    eur = exchange_rates.get_currancy_rate(order_items[0]["currency"])
    
    # order section
    order = frappe.get_doc({
        "doctype": 'Sales Order',
        "naming_series": "SO-KAUF-.YYYY.-",
        "customer": customer_name,
        "territory":territory,
        "order_type": "Sales",
        "po_no": id_order,
        "po_date": po_date,
        "transaction_date": po_date,
        "selling_price_list": selling.get_price_list(),
        "currency": order_items[0]["currency"],
        "conversion_rate": eur,
        "orderstatus": status_order,
        "items": sales_order_items,
        "payment_schedule": [{
            "idx": 1,
            "due_date": po_date,
            "invoice_portion": 100.0,
            "payment_term": payment.getPaymentTerm(),
            "doctype": "Payment Schedule",
        }]
    })
    
    try:
        order.insert()  
        add_comment_to_job(log, f"Sales order [{id_order}] added to {order.name}")
    except Exception as e:
        data_string = frappe.as_json(order)
        add_comment_to_job(log, f"Something went wrong: {e}, insert data: {data_string}")

#################################################################################################


def order_exist(id_order: str, log):
    sales_order = frappe.db.get_value(
        'Sales Order', {'po_no': id_order}, 'name')
    if sales_order:
        add_comment_to_job(
            log, f"Sales Order {id_order} exists under the name {sales_order}.")
        return True
    else:
        add_comment_to_job(
            log, f"Sales Order {id_order} does not exist in ErpNext. Start creating new document...")
        return False
