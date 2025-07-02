import random
import smtplib
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_email(email, otp):
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'

    from_email = 'jai@skylabstech.com'

    email_message = EmailMessage(subject, message, from_email, [email])
    email_message.send()



def send_welcome_email(self, email):
        subject = 'Welcome to YourApp!'
        html_message = render_to_string('welcome_email_template.html', {'email': email})
        plain_message = strip_tags(html_message)
        from_email = 'jai@skylabstech.com'  # Replace with your email
        recipient_list = [email]

        email = EmailMessage(subject, plain_message, from_email, recipient_list)
        email.content_subtype = "html"
        email.send()



# def send_otp(api_key, sender, mobile, otp):
#     url = "https://www.fast2sms.com/dev/bulkV2"  # Replace with your SMS provider's URL
#     api_key = "5GrHl3TveRQV2I6NwSfYCzFj01JXdLxWkBnAM4ut8pagcbPm9ODNrALnQ1bR5yUYCOd7xSK9PklHzfjG"
#     headers = {
#         'Authorization': f'Bearer {api_key}',  # Update if API key is sent in headers
#         'Content-Type': 'application/json',
#         'Cache-Control': "no-cache",
#     }
#     data = {
#         'sender': sender,
#         'mobile': mobile,
#         'message': f'Your OTP is {otp}.',
#     }
#     response = requests.post(url, headers=headers, json=data)
#     return response.json()