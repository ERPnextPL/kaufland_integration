import frappe


def update():
    frappe.msgprint(
    msg='This file does not exist',
    title='Error',
    raise_exception=FileNotFoundError
)