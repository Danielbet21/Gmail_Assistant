from email.utils import parseaddr
from simplegmail import Gmail , message
from simplegmail.query import construct_query
from datetime import datetime, timedelta
import os
import pymongo
import logging
import sqlite_file

logging.basicConfig(level=logging.INFO)


client = pymongo.MongoClient("mongodb://localhost:27017/")

gmail = Gmail()

def get_name_from_email(email) -> str:

    return str(email.split('@')[0])


def get_labels(labels, indicator:int)-> list[str]:
    # indicator = 0 :from gmail, 1: from mongo
    label_names = None
    if labels != None:
        if indicator == 0:
            labels = labels.split(',')
            label_names = [label.split("'")[1] for label in labels]
            label_names = list(set(label_names))
        else:
            label_names = [label.name for label in labels]
            
    return label_names


def get_message_by_id_from_gmail(desired_message_id: str, date: str, subject: str)-> message.Message:
    query = {
        "subject":subject
        }
    messages = gmail.get_messages(query=construct_query(**query))
    for message in messages:
        if message.id == desired_message_id:
            sqlite_file.process_attachments(message.id, message.attachments)
            return message
    

def get_email_sender_name(message: str) -> str:
    
    return parseaddr(message)[0]


def get_messages_inbox()-> list[message.Message]:

        params = {
            "labels": "INBOX"
        }

        messages = gmail.get_messages(query=construct_query(params))
        return messages