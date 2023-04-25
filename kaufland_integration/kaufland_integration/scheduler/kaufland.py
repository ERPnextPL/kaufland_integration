import frappe
import json
from frappe.core.doctype.rq_job.rq_job import JOB_STATUSES
from frappe.utils import now_datetime
from rq.job import Job, JobStatus
from rq.registry import StartedJobRegistry
from rq import get_current_job, Connection, Queue
from frappe.utils.background_jobs import get_queue, get_queues
import pdb

import time
import hmac
import hashlib


def delete_jobs_on_uninstall():
    with Connection():
        queues = get_queues()
        for queue in queues:
            jobs = Job.fetch_many(queue.job_ids, connection=queue.connection)
            for job in jobs:
                if job.origin == 'kaufland.get_order':
                    job.delete()

    frappe.db.delete('Scheduled Job Type', {'name': 'kaufland.get_order'})
    frappe.db.commit()

# def install():
#    frappe.utils.background_jobs.enqueue(
#     job_name="test",
#     method="kaufland_integration.kaufland_integration.scheduler.kaufland.test",
#     queue='long')


def uninstall():
    delete_jobs_on_uninstall()

    # frappe.utils.background_jobs.cancel(
    #     job_name="test",
    #     method='kaufland_integration.kaufland_integration.scheduler.kaufland.test',
    #     queue='long',
    # )


def add_comment(comment):
    last_log = frappe.get_last_doc("Scheduled Job Log", filters={"scheduled_job_type": "kaufland.get_order", "status":"Start"},order_by="creation desc")
    frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": "Scheduled Job Log",
        "reference_name": last_log.name,
        "content": comment
    }).insert(ignore_permissions=True)


def sign_request(method, uri, body, timestamp, secret_key):
    plain_text = "\n".join([method, uri, body, str(timestamp)])

    digest_maker = hmac.new(secret_key.encode(), None, hashlib.sha256)
    digest_maker.update(plain_text.encode())
    return digest_maker.hexdigest()


def get_order():
    job = get_current_job()
    add_comment("mmmmm "+str(job))

