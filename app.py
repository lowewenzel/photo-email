# photo-email by wenzel
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from email_validator import validate_email, EmailNotValidError
from sendgrid.helpers.mail import *


class PhotoSubject():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.files = []

running = True
subjects = []


def send_email():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("wenzel@wrlowe.com")
    to_email = Email("lowewenzel@gmail.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def input_email():
    email = input("Email: ")
    try:
        v = validate_email(email)  # validate and get info
        email = v["email"]  # replace with normalized form
        return email
    except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
        print("\n", str(e))
        return input_email()


def create_subject():
    user_name = input("Name: ")
    user_email = input_email()
    new_user = PhotoSubject(user_name, user_email)
    return new_user


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(event.src_path[6:])
        subjects[-1].files.append(event.src_path[6:])
        print(subjects[-1].files)

def main():
    while running:
        os.system('clear')
        print("Wenzel's photo-email script!\n\n")
        subjects.append(create_subject())  # Append new subject to list

        os.system('clear')
        print("Wenzel's photo-email script!\n\n")
        print(subjects[-1].name)
        print(subjects[-1].email)
        print("\nGet ready to smile!\n\n")

        path = './img'
        observer = Observer()
        handler = FileHandler()
        observer.schedule(handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        input("Press enter to start new subject\n")  # hold
        file = open("subjects.txt", "a")
        file.write("\n" + subjects[-1].name + "\n")
        file.write(subjects[-1].email + "\n")
        for i in subjects[-1].files:
            file.write(i + "\n")
        file.close()



main()
