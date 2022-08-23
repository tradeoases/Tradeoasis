from dis import dis
from django.contrib.auth.models import User
from supplier import models as SupplierModels
from manager import models as ManagerModels

def categories_showroows(request):
    context = dict()
    context['categories_header'] = SupplierModels.ProductCategory.objects.all().order_by("-id")[:6]
    context['showroows_headers'] = ManagerModels.Showroom.objects.all().order_by("-id")[:6]

    return context