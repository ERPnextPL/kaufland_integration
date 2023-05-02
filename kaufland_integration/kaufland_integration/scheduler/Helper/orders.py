import json
import requests
import time
import hmac
import hashlib
import urllib.parse
import frappe
from kaufland_integration.kaufland_integration.doctype.kaufland_setings.kaufland_setings import KauflandCredentials
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext import order_exist
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job, set_job_async, set_job_for_order_async


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


def get_orders_form_kaufland(dateFrom: str,log):
   
    params = {'storefront': 'de', 'fulfillment_type': 'fulfilled_by_merchant',
              'ts_created_from_iso': dateFrom}
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
                          methodPath=f"kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.create_order_from_kaufland_data", queue="default", data=data["data"], log=log)
    else:
        add_comment_to_job(log, f"No data for order {id_order}")

#################################################################################################
