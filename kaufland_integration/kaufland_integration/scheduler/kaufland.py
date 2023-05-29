import frappe
from datetime import datetime, timedelta
from kaufland_integration.kaufland_integration.doctype.kaufland_setings.kaufland_setings import KauflandSettingsOptions
from kaufland_integration.kaufland_integration.scheduler.Helper.orders import get_orders_form_kaufland
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job, set_job_for_order_async

def get_orders():
    settings = KauflandSettingsOptions() 

    last_log = frappe.get_last_doc("Scheduled Job Log", filters={"scheduled_job_type": "kaufland.get_orders", "status": "Start"}, order_by="creation desc")
    add_comment_to_job(last_log,f"Start process at: {datetime.now()} ")

    current_date = datetime.now()
    days_to_subtract = settings.number_of_days_back
    if days_to_subtract is not None:
        date_after_subtract = current_date - timedelta(days=days_to_subtract)
    else:
        date_after_subtract = current_date
        
    date = date_after_subtract.date().isoformat() + "T00:00:00Z" 

    orders = get_orders_form_kaufland(date,last_log)
    if orders != None:
        add_comment_to_job(last_log,f"List of orders retrieved from date {date}: {str(orders)} ")
        for id in orders:           
            set_job_for_order_async(f"kaufland.get_order={id}",f"kaufland_integration.kaufland_integration.scheduler.Helper.orders.get_order_form_kaufland_by_id","default",id,last_log)
    
