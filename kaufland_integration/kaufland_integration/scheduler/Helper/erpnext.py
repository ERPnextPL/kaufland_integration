import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job
import gender_guesser.detector as gender
from countryinfo import CountryInfo

#################################################################################################


def create_order_from_kaufland_data(data, log):
    buyer = data["buyer"]
    biling_adrress = data["billing_address"]
    shipping_address = data["shipping_address"]

    # create customer
    if not customer_exist(buyer["email"],log):
        create_customer(data,log)

    
    # salutation = get_salutation(biling_adrress["first_name"],country)
    # if not check_if_salutation_exist(salutation,log):
    #     create_salutation(salutation)


#################################################################################################

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


def get_contry_name_by_code(contry_code):
    return str(CountryInfo(contry_code).name()).lower().capitalize()


def get_currency_by_code(contry_code):
    currencyList = CountryInfo(contry_code).currencies()
    if isinstance(currencyList, list):
        return str(currencyList[0]).upper()
    else:
        return str(currencyList).upper()


def get_gender_by_name(name, contry_code):
    return gender.Detector(case_sensitive=False).get_gender(name=name, country=get_contry_name_by_code(contry_code))


def get_salutation(pname, pcountry):
    match pcountry:
        case "de":
            match get_gender_by_name(pname, pcountry):
                case "male":
                    return "Herr"
                case "female":
                    return "Frau"
                case _:
                    return "unknown"
        case "en":
            match get_gender_by_name(pname, pcountry):
                case "male":
                    return "Mr"
                case "female":
                    return "Ms"
                case _:
                    return "unknown"


def check_if_salutation_exist(salutation, log):
    salut = frappe.db.get_value('Salutation', {'name': salutation}, 'name')
    if salut:
        return True
    else:
        add_comment_to_job(
            log, f"Salutation '{salutation}' does not exist in ErpNext. Adding new salutation")
        return False


def customer_exist(customer_email, log):
    customer = frappe.db.get_value(
        'Customer', {'email_id': customer_email}, 'name')
    if customer:
        return True
    else:
        add_comment_to_job(
            log, f"Customer '{customer_email}' does not exist in ErpNext. Adding new Customer")
        return False


def country_exist(coutry_name, log):
    country = frappe.db.get_value('Country', {'name': coutry_name}, 'name')
    if country:
        return True
    else:
        add_comment_to_job(
            log, f"Country '{coutry_name}' does not exist in ErpNext. Adding new country")
        return False
 
def get_territory(country_name):
    territory = frappe.db.get_value('Territory', {'name': country_name}, 'name')
    if territory is not None:
        return str(territory)
    else:
        territory = frappe.get_doc({
            "doctype": "Territory",
            "territory_name": country_name
        })
        territory.insert()
        return str(territory.name)
    
def get_customer_group():
    customer_group = frappe.db.get_value('Customer Group', {'name': 'Kaufland.de'}, 'name')
    if customer_group is not None:
        return str(customer_group)
    else:
        group = frappe.get_doc({
            "doctype": "Customer Group",
            "name": "Kaufland.de",
            "customer_group_name": "Kaufland.de"
        })
        group.insert()
        return str(group.name)

def get_customer_type(company_name):    
    if company_name == '' or company_name is None:
        return "Individual"
    else:
        return "Company"

def address_exist(address_id, address_type, log):
    address = frappe.db.get_value(
        'Address', {'address_title': address_id, "address_type": address_type}, 'name')
    if address:
        return True
    else:
        add_comment_to_job(
            log, f"{address_type} address '{address_id}' does not exist in ErpNext. Adding new address")
        return False


def create_customer(data,log):
    buyer = data["buyer"]
    biling_adrress = data["billing_address"]
    shipping_address = data["shipping_address"]
    if buyer is not None and biling_adrress is not None and shipping_address is not None:
        country_code = str(biling_adrress["country"]).lower()
        country_currency = get_currency_by_code(country_code)

        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": biling_adrress["first_name"] + " " + biling_adrress["last_name"],
            "mobile_no": shipping_address["phone"],
            "email_id": buyer["email"],
            "language": country_code,
            "default_currency": country_currency,
            "customer_type": get_customer_type(biling_adrress["company_name"]),
            "customer_group": get_customer_group(),
            "territory": get_territory(get_contry_name_by_code(country_code)) 
        })
        customer.insert()
        if frappe.db.exists("Customer", customer.name):
            # create address
            if biling_adrress is not None:
                country_code = str(biling_adrress["country"]).lower()
                country_name = get_contry_name_by_code(country_code)
                address_title = biling_adrress["first_name"] + " " + biling_adrress["last_name"]
                if not country_exist(country_name, log):
                    create_country(country_name, country_code)
                if not address_exist(address_title, "Billing", log):
                    create_address(biling_adrress, "Billing", country_name, country_code, buyer["email"],customer)
        
            if shipping_address is not None:
                country_code = str(shipping_address["country"]).lower()
                country_name = get_contry_name_by_code(country_code)
                address_title = shipping_address["first_name"] +  " " + shipping_address["last_name"]
                if not country_exist(country_name, log):
                    create_country(country_name, country_code)
                if not address_exist(address_title, "Shipping", log):
                    create_address(shipping_address, "Shipping", country_name, country_code, "",customer)
        else:
            add_comment_to_job(
            log, f"Customer '{customer.name}' does not exist in ErpNext. Insert Error...")


def create_address(addressData, address_type, country_name, country_code, email,customer):
    
    primary = 0
    shipping = 0
    is_company_address = 0
    title = ""
    
    if address_type == "Billing":
        primary = 1
        if get_customer_type(addressData["company_name"]) == "Company": 
            is_company_address = 1
            title = addressData["company_name"]
        else:
            is_company_address = 0
            title = addressData["first_name"] + " " + addressData["last_name"]
    elif address_type == "Shipping":
        shipping = 1
        title = addressData["first_name"] + " " + addressData["last_name"]
             
    address = frappe.get_doc({
        "doctype": "Address",
        "address_title": title,
        "address_type": address_type,
        "address_line1": addressData["street"],
        "address_line2": addressData["house_number"],
        "city": addressData["city"],
        "county": country_code,
        "country": country_name,
        "pincode": addressData["postcode"],
        "email_id": email,
        "phone": addressData["phone"],
        "is_primary_address": primary,
        "is_shipping_address": shipping,
        "links":[{
            "link_doctype": "Customer", 
            "link_name": customer.name 
        }],
        "is_your_company_address": is_company_address
    })
    address.insert()


def create_salutation(name):
    salutation = frappe.get_doc({
        "doctype": "Salutation",
        "name": name,
        "salutation": name
    })
    salutation.insert()


def create_country(country_name, coutry_code):
    country = frappe.get_doc({
        "doctype": "Country",
        "name": country_name,
        "country_name": country_name,
        "date_format": "dd-mm-yyyy",
        "time_format": "HH:mm:ss",
        "code": coutry_code
    })
    country.insert()
