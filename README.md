# Python Custom Photobooth
A command-line photobooth application that reads incoming photos from folders and attaches them to users who use the photobooth.

## Instructions

### Requirements
You need:
- sendgrid.env (sendgrid API)
- credentials.json (gdrive API)
- token.json (gdrive API)

`pip install` the following:
- `oauth2client`
- `googleapiclient`
- `httplib2`
- `watchdog`
- `email_validator`
- `sendgrid`
- `phonenumbers`

Modify `send_email` to your liking for email from, subject, and content.

### Starting the application
1. Have your camera system export photos to the folder specified, in my case, I used Canon EOS utility.
2. Run `python app.py [folder to look for photos]` to start the photobooth.
3. Have the subject enter their information (name, email, phone/telegram)
4. Take pictures (program will read incoming files only), then press enter for new subject
5. Once finished, exit the application
6. Run `python app.py send` to start sending process.
