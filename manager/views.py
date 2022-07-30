from unicodedata import category
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q

# apps
from supplier.models import Product, ProductCategory, Store
from manager.models import Showroom


class HomeView(View):
    template_name = "manager/home.html"

    def get(self, request):
        context_data = {
            "view_name": "Home",
            'product_categories' : {
                'context_name' : 'product-categories',
                'results' : ProductCategory.objects.all().order_by('-created_on')
            },
            'showrooms' : {
                'context_name' : 'showrooms',
                'results' : Showroom.objects.all()[:6]
            },
            'stores' : {
                'context_name' : 'stores',
                'results' : Store.objects.all()[:6]
            },
            'products' : {
                'context_name' : 'products',
                'results' : Product.objects.all()[:6]
            },
            'new_arrivals' : {
                'context_name' : 'new-arrivals',
                'results' : Product.objects.all()[:6]
            }
        }
        return render(request, self.template_name, context=context_data)

class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'Product'
        context['product_categories'] = {
            'context_name' : 'product-categories',
            'results' : ProductCategory.objects.all().order_by('-created_on')
        }
        return context

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_queryset().first()
        context['view_name'] = product.name
        context['product_categories'] = {
            'context_name' : 'product-categories',
            'results' : ProductCategory.objects.all().order_by('-created_on')
        }
        context['related_products'] = {
            'context_name' : 'related-product',
            'results' : Product.objects.filter(Q(category = product.category), ~Q(id = product.id))
        }
        return context