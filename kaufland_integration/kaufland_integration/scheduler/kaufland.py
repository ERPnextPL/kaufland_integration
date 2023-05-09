import frappe
from datetime import datetime, timedelta
from kaufland_integration.kaufland_integration.scheduler.Helper.orders import get_orders_form_kaufland
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job, set_job_for_order_async

def get_orders():
    last_log = frappe.get_last_doc("Scheduled Job Log", filters={"scheduled_job_type": "kaufland.get_orders", "status": "Start"}, order_by="creation desc")
    today = datetime.now().date().isoformat() + "T00:00:00Z" 
    
    orders = get_orders_form_kaufland(today,last_log)
    if orders != None:
        add_comment_to_job(last_log,f"Orders for date {today}: {str(orders)} ")
        for id in orders:           
            set_job_for_order_async(f"kaufland.get_order={id}",f"kaufland_integration.kaufland_integration.scheduler.Helper.orders.get_order_form_kaufland_by_id","default",id,last_log)
