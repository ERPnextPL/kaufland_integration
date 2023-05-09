import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job


class Payment:
    def __init__(self):
        self.payment = None

    def getPaymentTerm(self):      
        return "Portal payment"
    
    def createPaymentTerm(self):
        term = frappe.get_doc({ 
            "doctype": "Payment Term",
            "payment_term_name": 'Portal payment',
            "invoice_portion":"100",
            "mode_of_payment":"Przelew",
            "description":"Płatności dokonane przez portale aukcyjne"   #todo dodać translacje
        })
        term.insert()

           
    def ifAddPortalPaymentTerm(self):
        payment = frappe.db.get_value('Payment Term',{'name': 'Portal payment'}, 'name')
        if payment is not None:
            return False
        else:
            return True
    
    def addKauflandPayments(self):
        if self.ifAddPortalPaymentTerm():
            self.createPaymentTerm() 

    def deletePaymentTerm(self):
        frappe.delete_doc("Payment Term", 'Portal payment')
        frappe.db.commit()