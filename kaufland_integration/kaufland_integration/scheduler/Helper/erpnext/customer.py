import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job
from countryinfo import CountryInfo


class Customer:
    def __init__(self):
        self.customer = None
        self.country = None
        self.address = None

    def __get_contry_name_by_code(self, contry_code):
        return str(CountryInfo(contry_code).name()).lower().capitalize()

    def __get_currency_by_code(self, contry_code):
        currencyList = CountryInfo(contry_code).currencies()
        if isinstance(currencyList, list):
            return str(currencyList[0]).upper()
        else:
            return str(currencyList).upper()

    def customer_exist(self,customer_email, log):
        customer = frappe.db.get_value('Customer', {'email_id': customer_email}, 'name')
        if customer:
            return True
        else:
            add_comment_to_job(log, f"Customer '{customer_email}' does not exist in ErpNext. Adding new Customer")
            return False

    def __contact_exist(self,contact_email):
        contact_email = frappe.db.get_value('Contact', {'email_id': contact_email}, 'name')
        if contact_email:
            return True
        else:
            return False

    def __country_exist(self,coutry_name, log):
        country = frappe.db.get_value('Country', {'name': coutry_name}, 'name')
        if country:
            return True
        else:
            add_comment_to_job( log, f"Country '{coutry_name}' does not exist in ErpNext. Adding new country")
            return False

    def __get_territory(self,country_name):
        territory = frappe.db.get_value('Territory', {'name': country_name}, 'name')
        if territory is not None:
            return str(territory)
        else:
            territory = frappe.get_doc({ "doctype": "Territory", "territory_name": country_name })
            territory.insert()
            return str(territory.name)

    def __get_customer_group(self):
        customer_group = frappe.db.get_value('Customer Group', {'name': 'Kaufland.de'}, 'name')
        if customer_group is not None:
            return str(customer_group)
        else:
            group = frappe.get_doc({ "doctype": "Customer Group", "name": "Kaufland.de", "customer_group_name": "Kaufland.de" })
            group.insert()
            return str(group.name)

    def __get_customer_type(self,company_name):
        if company_name == '' or company_name is None:
            return "Individual"
        else:
            return "Company"

    def __address_exist(self,address_id, address_type, log):
        address = frappe.db.get_value('Address', {'address_title': address_id, "address_type": address_type}, 'name')
        if address:
            return True
        else:
            add_comment_to_job(log, f"{address_type} address '{address_id}' does not exist in ErpNext. Adding new address")
            return False

    def create_customer(self,data, log):
        buyer = data["buyer"]
        biling_adrress = data["billing_address"]
        shipping_address = data["shipping_address"]

        if buyer is not None and biling_adrress is not None and shipping_address is not None:
            country_code = str(biling_adrress["country"]).lower()
            country_currency = self.__get_currency_by_code(country_code)

            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": biling_adrress["first_name"] + " " + biling_adrress["last_name"],
                "mobile_no": shipping_address["phone"],
                "email_id": buyer["email"],
                "language": country_code,
                "default_currency": country_currency,
                "customer_type": self.__get_customer_type(biling_adrress["company_name"]),
                "customer_group": self.__get_customer_group(),
                "territory": self.__get_territory(self.__get_contry_name_by_code(country_code))
            })
            customer.insert()

            if frappe.db.exists("Customer", customer.name):
                # create address
                if biling_adrress is not None:
                    country_code = str(biling_adrress["country"]).lower()
                    country_name = self.__get_contry_name_by_code(country_code)
                    address_title = biling_adrress["first_name"] + " " + biling_adrress["last_name"]
                    if not self.__country_exist(country_name, log):
                        self.__create_country(country_name, country_code)
                    if not self.__address_exist(address_title, "Billing", log):
                        self.__create_address(biling_adrress, "Billing", country_name, country_code, buyer["email"], customer)

                if shipping_address is not None:
                    country_code = str(shipping_address["country"]).lower()
                    country_name = self.__get_contry_name_by_code(country_code)
                    address_title = shipping_address["first_name"] + " " + shipping_address["last_name"]
                    if not self.__country_exist(country_name, log):
                        self.__create_country(country_name, country_code)
                    if not self.__address_exist(address_title, "Shipping", log):
                        self.__create_address(shipping_address, "Shipping", country_name, country_code, "", customer)
            else:
                add_comment_to_job(log, f"Customer '{customer.name}' does not exist in ErpNext. Insert Error...")
                

    def __create_address(self,addressData, address_type, country_name, country_code, email, customer):

        primary = 0
        shipping = 0
        is_company_address = 0
        title = ""

        if address_type == "Billing":
            primary = 1
            if self.__get_customer_type(addressData["company_name"]) == "Company":
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
            "links": [{
                "link_doctype": "Customer",
                "link_name": customer.name
            }],
            "is_your_company_address": is_company_address
        })
        address.insert()

        if address_type == "Billing":

            contact = None
            if not self.__contact_exist(email):
                contact = self.__create_contact(address, customer)

            primary_address = f"{address.address_line1} {address.address_line2}<br>{address.pincode} {address.city}<br>\n{address.country}"
            customer.primary_address = primary_address
            customer.customer_primary_address = address.name
            if contact is not None:
                customer.customer_primary_contact = contact.name
                customer.email_id = contact.email_id
            customer.save()

    def __create_contact(self,data, customer):
        splited_name = data.address_title.split()

        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": splited_name[0],
            "last_name": splited_name[1],
            "phone": data.phone,
            "email_ids": [
                {
                    "email_id": data.email_id,
                    "is_primary": 1,
                    "parent": data.address_title,
                    "parentfield": "email_ids",
                    "parenttype": "Contact",
                    "doctype": "Contact Email"
                }
            ]
        })
        contact.insert()

        # Create a new dynamic link record
        link_doc = frappe.new_doc("Dynamic Link")
        link_doc.link_doctype = "Customer"
        link_doc.link_name = customer.name
        link_doc.parenttype = "Contact"
        link_doc.parent = contact.name
        link_doc.insert(ignore_permissions=True)

        contact.append("links", {
            "link_doctype":  "Customer",
            "link_name":  customer.name
        })
        contact.save()

        return contact


    def __create_country(self,country_name, coutry_code):
        country = frappe.get_doc({
            "doctype": "Country",
            "name": country_name,
            "country_name": country_name,
            "date_format": "dd-mm-yyyy",
            "time_format": "HH:mm:ss",
            "code": coutry_code
        })
        country.insert()
