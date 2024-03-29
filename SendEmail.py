import smtplib
import ssl
from email.message import EmailMessage
import random
email_sender="arieldob13@gmail.com"
email_password="rmmp cuba nxam kdvx"
email_receiver="arieldob13@gmail.com"
subject="Password change code"

# Add SSL (layer of security)
context = ssl.create_default_context()
def send_email(email_receiver):
    body = "Hi here is the code to change your password "+generate_four_digit_number()
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# Log in and send the email



def generate_four_digit_number():
    number = random.randint(1, 1000)
    if number < 10:  # If the number is two-digit, add two zeros at the beginning
        return f"00{number}"
    elif number < 100:  # If the number is three-digit, add one zero at the beginning
        return f"0{number}"
    else:
        return str(number*10)  # If the number is already four-digit, return it as is


