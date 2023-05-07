import frappe
from kaufland_integration.kaufland_integration.scheduler.Helper.jobs import add_comment_to_job


class Payment:
    def __init__(self):
        self.payment = None

