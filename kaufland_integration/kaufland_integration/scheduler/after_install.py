import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.payment import Payment


def install():
    last_log = frappe.get_last_doc("Scheduled Job Log", filters={"scheduled_job_type": "kaufland.get_orders", "status": "Start"}, order_by="creation desc")
    payment = Payment(last_log)
    payment.addKauflandPayments()