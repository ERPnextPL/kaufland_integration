import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job
import gender_guesser.detector as gender
from countryinfo import CountryInfo


def check_if_order_exist(id_order: str, log):
    sales_order = frappe.db.get_value(
        'Sales Order', {'po_no': id_order}, 'name')

    if sales_order:
        add_comment_to_job(
            log, f"Sales Order {id_order} exists under the name {sales_order}.")
        return True
    else:
        add_comment_to_job(
            log, f"Sales Order {id_order} does not exist in ErpNext. Start creating new document...")
        return False


def create_order_from_kaufland_data(dataOrder, log):
    print("")

def get_contry_name_by_code(contry_code):
    return CountryInfo(contry_code).name()

def get_gender_by_name(name,contry_code):
    return gender.Detector(case_sensitive=False).get_gender(name=name,country=get_contry_name_by_code(contry_code))

def get_salutation(pname, pcountry):
    match pcountry:
        case "de":
            match get_gender_by_name(pname,pcountry):
                case "male":
                    return "Herr"
                case "female":
                    return "Frau"
                case _:
                    return ""
        case "en":
            match get_gender_by_name(pname,pcountry):
                case "male":
                    return "Herr"
                case "female":
                    return "Frau"
                case _:
                    return ""
   