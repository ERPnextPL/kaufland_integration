import json
import pdb
import requests
import time
import hmac
import hashlib
import urllib.parse
from datetime import datetime
import frappe
from kaufland_integration.kaufland_integration.doctype.kaufland_setings.kaufland_setings import KauflandCredentials
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job
from rq import get_current_job


def get_headers(url:str,timestamp:int):
    creditionals = KauflandCredentials()
    return {
        'Accept':'application/json',
        'Shop-Client-Key': creditionals.key,
        'Shop-Timestamp': str(timestamp),
        'Shop-Signature': sign_request('GET', url,'', timestamp, creditionals.key_secret)
    }

def sign_request(method, uri, body, timestamp, secret_key):
    plain_text = "\n".join([method, uri, body, str(timestamp)])
    digest_maker = hmac.new(secret_key.encode(), None, hashlib.sha256)
    digest_maker.update(plain_text.encode())
    return digest_maker.hexdigest()

def get_orders_form_kaufland(dateFrom:str):
    params = {'storefront': 'de', 'fulfillment_type': 'fulfilled_by_merchant','ts_created_from_iso':dateFrom}
    uri = f'https://sellerapi.kaufland.com/v2/orders?{urllib.parse.urlencode(params)}'
    timestamp = int(time.time())
    response = requests.get(uri, headers=get_headers(uri,timestamp))
    data = json.loads(response.content.decode("utf-8") )
    return [id_order["id_order"] for id_order in data["data"]]


def get_order_by_id(id_order:str):
    job = get_current_job()
    pdb.set_trace() 
    log =  frappe.get_last_doc("RQ Job", filters={"job_id": job.id ,"status": "queued"}, order_by="creation desc")
    params = {'embedded': 'order_invoices'}
    uri = f'https://sellerapi.kaufland.com/v2/orders/{id_order}?{urllib.parse.urlencode(params)}'
    timestamp = int(time.time())
    response = requests.get(uri, headers=get_headers(uri,timestamp))
    data = json.loads(response.content.decode("utf-8") )
    add_comment_to_job(log,f"Order[{id_order}]: {str(data)}")

    return data["data"]
