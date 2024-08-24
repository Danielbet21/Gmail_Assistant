from simplegmail import Gmail
from datetime import datetime
import shared_resources
from apscheduler.triggers.interval import IntervalTrigger
import requests
import data_base



class SchedulerManager:
    @staticmethod
    def check_emails(gmail, user_email):
        messages = gmail.get_unread_inbox()
        if messages:
            data_base.insert_many_documents_to_collection("Messages", messages)
            messages = [{message.id:data_base.labels_to_list(message.label_ids)} for message in messages]
            for message in messages:
                for id_num, labels in message.items():
                    for label in labels:
                            data_base.insert_id_to_Users_by_label(user_email, label, id_num)


    @staticmethod
    def start_scheduler(scheduler, gmail, user_email):
        # Add a job to the scheduler
        scheduler.add_job(
            func=SchedulerManager.check_emails,
            trigger=IntervalTrigger(minutes=5),  # Run every 1 minutes
            id='check_emails_job',
            name='Check emails every 5 minutes',
            replace_existing=True,
            kwargs={'gmail': gmail, 'user_email': user_email}
        )
        scheduler.start()
