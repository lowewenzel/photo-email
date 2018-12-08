# photo-email by wenzel
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from __future__ import print_function
from oauth2client import file, client, tools
from googleapiclient.discovery import build, MediaFileUpload
from httplib2 import Http
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from email_validator import validate_email, EmailNotValidError
from sendgrid.helpers.mail import *
import sendgrid
import os
import sys
import time
import logging
import phonenumbers


class FileHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if "JPG" in event.src_path and "TMP" not in event.src_path:
            subjects[-1].files.append(event.src_path[5:])
        print(subjects[-1].files)


class PhotoSubject():
    def __init__(self, name=None, email=None, telegram=None):
        self.name = name if name is not None else None
        self.email = email if email is not None else None
        self.telegram = telegram if telegram is not None else None
        self.files = []


running = False
subjects = []
SCOPES = 'https://www.googleapis.com/auth/drive.file'


def send_email(subject_user, drive_link):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("lowewenzel@gmail.com")
    to_email = Email(subject_user.email)
    subject = "Career and Livelihood Fair LinkedIn Portraits"
    content = Content("text/html",
                      "Hey " + subject_user.name +
                      ",<br><br>Here are your LinkedIn Photobooth portraits!" +
                      "<br><br>" + drive_link + "<br><br>Wenzel via SendGrid")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


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
    user_telegram = input("Telegram Username or Phone Number: ")
    new_user = PhotoSubject(user_name, user_email, user_telegram)
    return new_user


def auth_drive():
    global file
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service


def change_permissions(drive_service, file_id, email):
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))
    batch = drive_service.new_batch_http_request(callback=callback)
    print(email)
    user_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    batch.add(drive_service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
    ))
    batch.execute()


def upload_files(service, subject):
    subject_name = subject.name

    folder_metadata = {
                        'name': subject.name,
                        'mimeType': 'application/vnd.google-apps.folder'
                        }
    folder = service.files().create(body=folder_metadata,
                                          fields='id').execute()
    folder_id = folder.get('id')
    change_permissions(service, folder_id, subject.email)
    print(folder.get('id'))

    for file_name in subject.files:
        file_metadata = {
                         'name': file_name,
                         'parents': [folder_id]
                         }
        media = MediaFileUpload('5D/export/' + file_name,
                                mimetype='image/jpeg')
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
    send_email(subject, 'https://drive.google.com/drive/folders/' + folder.get('id'))

def main():
    appendable_subjects_file = open("subjects.txt", "a")
    while running:
        os.system('clear')
        print("Wenzel's photo-email script!\n\n")
        subjects.append(create_subject())  # Append new subject to list

        os.system('clear')
        print("Wenzel's photo-email script!\n\n")
        print(subjects[-1].name)
        print(subjects[-1].email)
        print(subjects[-1].telegram)
        print("\nGet ready to smile!\n\n")

        path = sys.argv[1]
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
        appendable_subjects_file.write("\n" + subjects[-1].name + "\n")
        appendable_subjects_file.write(subjects[-1].email + "\n")
        appendable_subjects_file.write(subjects[-1].telegram + "\n")
        for i in subjects[-1].files:
            appendable_subjects_file.write(i + "\n")
        appendable_subjects_file.close()
    readable_subjects_file = open("subjects.txt", "r")
    lines = [line for line in readable_subjects_file.readlines()]
    newVal = False
    new_user = PhotoSubject()
    count = 1
    service = auth_drive()
    for ln in lines:
        if ln.startswith('\n'):
            count = 0
            upload_files(service, new_user)
            new_user = PhotoSubject()
            count += 1
        elif count == 1:
            new_user.name = ln.replace('\n', '')
            count += 1
        elif count == 2:
            new_user.email = ln.replace('\n', '')
            count += 1
        elif count == 3:
            try:
                new_user.telegram = phonenumbers.format_number(phonenumbers.parse(
                                                               ln.replace('\n', ''), "US"),
                                                               phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                new_user.telegram = ln.replace('\n', '')
            count += 1
        else:
            new_user.files.append(ln.replace('\n', ''))
    readable_subjects_file.close()

main()
