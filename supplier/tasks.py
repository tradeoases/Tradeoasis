from celery.decorators import task
from celery.utils.log import get_task_logger

from supplier import models as SupplierModels

from django.utils.translation import get_language
from googletrans import Translator

translator = Translator()
from django.conf import settings

@task(name="make_model_translations")
def make_model_translations(fields, instance_id, modal_name):
    
    if modal_name == "Service":
        modal = SupplierModels.Service
    elif modal_name == "ServiceTag":
        modal = SupplierModels.ServiceTag
    elif modal_name == "Product":
        modal = SupplierModels.Product
    elif modal_name == "Store":
        modal = SupplierModels.Store
    elif modal_name == "ServiceTag":
        modal = SupplierModels.ServiceTag

    if modal_name in ["Product", "Store"]:
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
