from django.template import context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_account_activation_email(name, email, subject):
    context = {
        'name': name,
        'email': email,
        'review': subject
    }
    email_subject = subject
    email_body = render_to_string('/emails/email_message.html', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)