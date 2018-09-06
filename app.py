# photo-email by wenzel
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from email_validator import validate_email, EmailNotValidError
from sendgrid.helpers.mail import *


class PhotoSubject():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.files = []

running = True

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

def main():
    subjects = []
    while running:
        os.system('clear')
        print("Wenzel's photo-email script!\n\n")
        subjects.append(create_subject())  # Append new subject to list

        os.system('clear')
        print("Wenzel's photo-email script!\n\n")
        print(subjects[-1].name)
        print(subjects[-1].email)

        file = open("subjects.txt", "a")
        file.write("\n" + subjects[-1].name + "\n")
        file.write(subjects[-1].email + "\n")
        file.write("")

        input("\n\nGet ready to smile!\n\n\n\n\n\n\nPress enter to start new subject\n")  # hold



main()
