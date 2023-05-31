from requests import get
import frappe
from frappe.desk.moduleview import get, get_doctype_info, get_links_for_module





class Integration:
    def __init__(self):
        pass

    def add_links(self):
        try:
            self.__add_link_to_erpnext_integrations()
            print(f"* Adding link to ERPNext Integrations")
        except Exception as e:
            print(e)

    def delete_links(self):
        try:
            self.__dellete_link_from_erpnext_integrations()
            print(f"* Deleting link from ERPNext Integrations")
        except Exception as e:
            print(e)

    def __add_link_to_erpnext_integrations(self):
        workspace = frappe.get_doc("Workspace", {"name": "ERPNext Integrations"})
        workspace_links = workspace.get("links") or []
        new_link = {
            "hidden": 0,
            "is_query_report": 0,
            "label": "Kaufland Settings",
            "link_count": 0,
            "link_to": "Kaufland Setings",
            "link_type": "DocType",
            "onboard": 0,
            "type": "Link"
        }
        for index, link in enumerate(workspace_links, start=1):
            if link.get("label") == "Settings":
               workspace_links.insert(index,new_link)
        workspace.set("links", workspace_links)
        workspace.save()
        frappe.db.commit()

    def __dellete_link_from_erpnext_integrations(self):
        workspace = frappe.get_doc("Workspace", {"name": "ERPNext Integrations"})
        workspace_links = workspace.get("links") or []
        for link in workspace_links:
            if link.get("label") == "Kaufland Settings":
                workspace.links.remove(link)
                break

        workspace.save()
        frappe.db.commit()
