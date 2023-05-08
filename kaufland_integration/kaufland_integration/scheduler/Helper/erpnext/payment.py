import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job


class Payment:
    def __init__(self):
        self.payment = None

    def getPaymentTemplate():      
        return 'Kaufland.de'
    
    def createPaymentTempl(self):
        template = frappe.get_doc({ 
            "doctype": "Payment Terms Template",
            "template_name": 'Kaufland.de',
            "allocate_payment_based_on_payment_terms":'100'
        })
        template.insert()
    def createPaymentTerm(self):
        term = frappe.get_doc({ 
            "doctype": "Payment Term",
            "payment_term_name": 'Portal payment',
            "invoice_portion":"100"
        })
        term.insert()

    def ifAddKauflandPayment(self):
        payment = frappe.db.get_value('Payment Terms Template',{'name': 'Kaufland.de'}, 'name')
        if payment is not None:
            return False
        else:
        #    add_comment_to_job( self.log, f"Payment: 'Kaufland.de' does not exist in ErpNext. Adding new Item")
           return True 
           
    def ifAddPortalPaymentTerm(self):
        payment = frappe.db.get_value('Payment Term',{'name': 'Portal payment'}, 'name')
        if payment is not None:
            return False
        else:
        #    add_comment_to_job( self.log, f"Payment: 'Kaufland.de' does not exist in ErpNext. Adding new Item")
           return True
    
    def addKauflandPayments(self):
        if self.ifAddPortalPaymentTerm():
           self.createPaymentTerm() 
        if not self.ifAddKauflandPayment() :
            self.createPaymentTempl()

