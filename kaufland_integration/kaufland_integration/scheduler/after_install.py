import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.integrations import Integration
from kaufland_integration.kaufland_integration.scheduler.translations import translations
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.payment import Payment


def install():
    payment = Payment()
    payment.addKauflandPayments()
    
    translationsObj = translations()
    translationsObj.add_translations(translationsObj.get_translation_list())

    integrations = Integration()
    integrations.add_links()