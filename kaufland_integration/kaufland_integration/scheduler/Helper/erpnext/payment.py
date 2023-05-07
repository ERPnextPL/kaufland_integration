import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job


class Payment:
    def __init__(self, log):
        self.payment = None
        self.log = log

    def getPaymentTemplate():      
        return 'Kaufland.de'
    
    def createPaymentTempl(self,name):
        template = frappe.get_doc({
            "doctype": "Payment Terms Template ",
            "name": name
        })
        template.insert()

    def ifKauflandPaymentExist(self,log):
        payment = frappe.db.get_value('Payment Terms Template',{'name': 'Kaufland.de'}, 'name')
        if payment:
            return True
        else:
          #  add_comment_to_job(
            #    log, f"Payment: 'Kaufland.de' does not exist in ErpNext. Adding new Item")
            return False
    
    def addKauflandPayments(self):
        if self.ifKauflandPaymentExist():
            self.createPaymentTempl()

