from common.email_service import send_email
from InterviewIQ.celery import app


@app.task()
def send_email_task(template_path, data_dict, user, email_subject):
    send_email(template_path, data_dict, user, email_subject)
