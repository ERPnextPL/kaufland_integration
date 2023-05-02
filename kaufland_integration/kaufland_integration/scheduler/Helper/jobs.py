import frappe
from rq.job import Job
from rq import Connection
from frappe.utils.background_jobs import get_queues


def delete_all_jobs():
    with Connection():
        queues = get_queues()
        for queue in queues:
            jobs = Job.fetch_many(queue.job_ids, connection=queue.connection)
            for job in jobs:
                if job.origin == 'kaufland.get_orders':
                    job.delete()

    frappe.db.delete('Scheduled Job Type', {'name': 'kaufland.get_orders'})
    frappe.db.commit()


def set_job_for_order_async(jobName: str, methodPath: str, queue: str, id: str, log):
    frappe.enqueue(
        job_name=jobName,
        method=methodPath,
        is_async=True,
        queue=queue,
        id_order=id,
        log=log)

def set_job_async(jobName: str, methodPath: str, queue: str, data,log):
    frappe.enqueue(
        job_name=jobName,
        method=methodPath,
        is_async=True,
        queue=queue,
        data=data,
        log=log)


def cancel_single_job(jobName: str, methodPath: str, queue: str):
    frappe.utils.background_jobs.cancel(
        job_name=jobName,
        method=methodPath,
        queue=queue,
    )


def add_comment_to_job(reference, comment):
    frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": "Scheduled Job Log",
        "reference_name": reference.name,
        "content": comment
    }).insert(ignore_permissions=True)
