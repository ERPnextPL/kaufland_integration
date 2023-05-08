
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.payment import Payment

def install():
    payment = Payment()
    payment.addKauflandPayments()