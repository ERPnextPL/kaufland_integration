
from kaufland_integration.kaufland_integration.scheduler.translations import translations
from kaufland_integration.kaufland_integration.scheduler.Helper.erpnext.payment import Payment
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import delete_all_jobs


def uninstall():
    #
    payment = Payment()
    translationsObj = translations()

    # delete payments
    payment.deletePaymentTerm()
    
    # delete translations
    translationsObj.delete_translations(translationsObj.get_translation_list())
    
    # delete all jobs from queue
    delete_all_jobs()