import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job


def check_if_order_exist(id_order: str, log):
    sales_order = frappe.db.get_value('Sales Order', {'po_no': id_order}, 'name')

    if sales_order:
        add_comment_to_job(log, f"Sales Order {id_order} exists under the name {sales_order}.")
    else:
        add_comment_to_job(log, f"Sales Order {id_order} does not exist in ErpNext. Start creating new document...")
