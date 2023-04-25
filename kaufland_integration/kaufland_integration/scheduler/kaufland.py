import frappe
from datetime import datetime
from kaufland_integration.kaufland_integration.scheduler.Helper.orders import get_order_by_id, get_orders_form_kaufland
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job, run_single_job

def get_orders():
    last_log = frappe.get_last_doc("Scheduled Job Log", filters={"scheduled_job_type": "kaufland.get_orders", "status": "Start"}, order_by="creation desc")
    today = datetime.now().date().isoformat() + "T00:00:00Z" 
    orders = get_orders_form_kaufland(today)
    if orders != None:
        for id in orders:           
            run_single_job(f"kaufland.get_order={id}",f"kaufland_integration.kaufland_integration.scheduler.Helper.orders.get_order_by_id","default",id)
    add_comment_to_job(last_log,f"Orders: {str(orders)}")
