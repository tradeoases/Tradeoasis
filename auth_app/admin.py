from django.contrib import admin
from django.apps import apps

# Register your models here.
for model in apps.get_app_config('auth_app').get_models():
    try: 
        admin.site.register(model)
    except:
        pass