
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.payment import Payment
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import delete_all_jobs


def uninstall():
    payment = Payment()
    payment.deletePaymentTerm()
    delete_all_jobs()