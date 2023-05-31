from requests import get
import frappe
from frappe.desk.moduleview import get, get_doctype_info, get_links_for_module


def add_link_to_erpnext_integrations():
    workspace = frappe.get_doc("Workspace", {"name": "ERPNext Integrations"})
    print(workspace)
    workspace_links = workspace.get("links") or []
    print(workspace_links)
    # new_link = {
    #     "hidden": 0,
    #     "is_query_report": 0,
    #     "label": "Kaufland Settings",
    #     "link_count": 0,
    #     "link_to": "Kaufland Setings",
    #     "link_type": "DocType",
    #     "onboard": 0,
    #     "type": "Link"
    # }

    # workspace_links.append(new_link)
    # workspace.set("links", workspace_links)
    # workspace.save()


class Integration:
    def __init__(self):
        pass

    def get_links(self):
        pass
        # try:
        #     links = get_links_for_module("ERPNext", "ERPNext Integrations")
        #     info = get("ERPNext Integrations")
        #     print(info)
        #     add_link_to_erpnext_integrations()

        # except Exception as e:
        #     print(e)
