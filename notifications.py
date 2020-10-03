import requests
import urllib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_whatsapp_message(subject, msg):
    API_KEY = os.getenv('WHATSAPP_APIKEY')
    PHONE_NO = os.getenv('PHONE_NO')
    API_ENDPOINT = 'https://api.callmebot.com/whatsapp.php'
    msg = subject +':\n'+ msg
    encoded_msg = urllib.parse.quote(msg)
    params = {
        'phone': PHONE_NO,
        'text': encoded_msg,
        'apikey': API_KEY
    }
    params = "&".join('{}={}'.format(k,v) for k,v in params.items())
    response = requests.get(url=API_ENDPOINT, params=params)
    print('Whatsapp status code:',response.status_code)

def send_mail(subject, msg):
    message = Mail(
        from_email='khushdeep0002@gmail.com',
        to_emails='khushdeep02@gmail.com',
        subject=subject,
        plain_text_content=msg
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print('Email status code:',response.status_code)
    except Exception as e:
        print(e)
