from typing import List
from celery.decorators import task
from celery.utils.log import get_task_logger

from manager import models as ManagerModels

from django.utils.translation import get_language
from googletrans import Translator

translator = Translator()
from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import EmailMessage


@task(name="make_model_translations")
def make_model_translations(fields, instance_id, modal_name):


    if modal_name == "Service":
        modal = ManagerModels.Service
    elif modal_name == "Showroom":
        modal = ManagerModels.Showroom
    elif modal_name == "ProductCategory":
        modal = ManagerModels.ProductCategory
    elif modal_name == "ProductSubCategory":
        modal = ManagerModels.ProductSubCategory
    elif modal_name == "DiscussionReply":
        modal = ManagerModels.DiscussionReply
    elif modal_name == "Discussion":
        modal = ManagerModels.Discussion
    elif modal_name == "Promotion":
        modal = ManagerModels.Promotion

    if modal_name == "Discussion":
        instance = modal.admin_list.filter(id=instance_id).first()
    else:
        instance = modal.objects.filter(id=instance_id).first()
    
    
    make_translations(fields, instance, modal)


def make_translations(fields, instance, modal):
    for field in fields:
        for language in settings.LANGUAGES:
            try:
                if language[0] == get_language():
                    # already set
                    continue
                result = translator.translate(
                    getattr(instance, field), dest=language[0]
                )
                for model_field in modal._meta.get_fields():
                    if not model_field.name in f"{field}_{language[0]}":
                        continue

                    if model_field.name == f"{field}_{language[0]}":
                        setattr(instance, model_field.name, result.text)
                        instance.save()
            except:
                setattr(instance, f"{field}_{language[0]}", getattr(instance, field))
                instance.save()


@task(name="send_email")
def send_mail(subject: str, content : str, _to: List[str] = [], _reply_to: List[str] = [], _from=settings.DEFAULT_FROM_EMAIL):

    email_body = render_to_string(
        "email_message.html",
        {
            "content": "{}".format(content),
        },
    )
    email = EmailMessage(
        subject = subject,
        body = email_body,
        from_email = _from,
        to = _to,
        reply_to = _reply_to
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)

    # save email
    ManagerModels.SentEmail.objects.create(
        recipient = ", ".join(_to),
        subject = subject,
        sending_email = from_email,
        content = content,
        reply_to = ", ".join(_reply_to) if _reply_to else None
    )