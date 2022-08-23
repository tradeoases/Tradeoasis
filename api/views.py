from urllib import request
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from admin_api import serializers
from django.db.models import Q

from supplier import models as SupplierModels
from payment import models as PaymentModels

from admin_api import serializers
import supplier

class CustomListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

class LargeCustomListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"


class StoresListView(ListAPIView):
    serializer_class = serializers.StoreSerializer
    pagination_class = CustomListPagination

    def get_queryset(self):
        return SupplierModels.Store.objects.filter(supplier=self.request.user)

class ProductsListView(ListAPIView):
    serializer_class = serializers.ProductsSerializer
    pagination_class = CustomListPagination

    def get_queryset(self):
        return SupplierModels.Product.objects.filter(store__in = SupplierModels.Store.objects.filter(supplier=self.request.user))
        

class LoadingProductsListView(ListAPIView):
    serializer_class = serializers.ProductsSerializer
    pagination_class = LargeCustomListPagination
    queryset = SupplierModels.Product.objects.all()


class ContractsListView(ListAPIView):
    serializer_class = serializers.ContractsSerializer
    pagination_class = CustomListPagination

    def get_queryset(self):
        return PaymentModels.Contract.objects.filter(Q(buyer=self.request.user))

class ServicesListView(ListAPIView):
    serializer_class = serializers.ServiceSerializer
    pagination_class = CustomListPagination

    def get_queryset(self):
        return SupplierModels.Service.objects.filter(supplier=self.request.user)