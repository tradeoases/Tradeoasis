from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from admin_api import serializers

from auth_app import models as AuthModels
from supplier import models as SupplierModels
from buyer import models as BuyerModels
from manager import models as ManagerModels
from payment import models as PaymentModels
import supplier


class CustomListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class SupplierListView(ListAPIView):
    queryset = AuthModels.ClientProfile.objects.filter(user__account_type="SUPPLIER")
    serializer_class = serializers.SuppliersSerializer
    pagination_class = CustomListPagination

class SupplierRetrieveView(RetrieveAPIView):
    queryset = AuthModels.ClientProfile.objects.filter(user__account_type="SUPPLIER")
    serializer_class = serializers.SuppliersSerializer
    lookup_field = 'slug'


class BuyersListView(ListAPIView):
    queryset = AuthModels.ClientProfile.objects.filter(user__account_type="BUYER")
    serializer_class = serializers.BuyersSerializer
    pagination_class = CustomListPagination
    
class BuyerRetrieveView(RetrieveAPIView):
    queryset = AuthModels.ClientProfile.objects.filter(user__account_type="BUYER")
    serializer_class = serializers.BuyersSerializer
    lookup_field = 'slug'


class ProductsListView(ListAPIView):
    queryset = SupplierModels.Product.objects.all()
    serializer_class = serializers.ProductsSerializer
    pagination_class = CustomListPagination

class ProductRetrieveView(RetrieveAPIView):
    queryset = SupplierModels.Product.objects.all()
    serializer_class = serializers.ProductsSerializer
    pagination_class = CustomListPagination
    lookup_field = 'slug'

class SupplierProductsListView(ListAPIView):
    serializer_class = serializers.ProductsSerializer
    pagination_class = CustomListPagination
    lookup_field = 'slug'

    def get_queryset(self):
        supplier = AuthModels.ClientProfile.objects.filter(slug=self.kwargs.get('slug')).first()

        queryset = SupplierModels.Product.objects.filter(store__supplier = supplier.user)

        return queryset


class ContractsListView(ListAPIView):
    queryset = PaymentModels.Contract.objects.all()
    serializer_class = serializers.ContractsSerializer
    pagination_class = CustomListPagination

class ContractRetrieveView(RetrieveAPIView):
    queryset = PaymentModels.Contract.objects.all()
    serializer_class = serializers.ContractsSerializer
    pagination_class = CustomListPagination
    lookup_field = 'slug'


class ShowroowListView(ListAPIView):
    queryset = ManagerModels.Showroom.objects.all()
    serializer_class = serializers.ShowroomsSerializer
    pagination_class = CustomListPagination


class ManagerServicesListView(ListAPIView):
    queryset = ManagerModels.Service.objects.all()
    serializer_class = serializers.ManagerServicesSerializer
    pagination_class = CustomListPagination

class ManagerServiceRetrieveView(RetrieveAPIView):
    queryset = ManagerModels.Service.objects.all()
    serializer_class = serializers.ManagerServicesSerializer
    pagination_class = CustomListPagination
    lookup_field = 'slug'

class MembershipListView(ListAPIView):
    queryset = PaymentModels.Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    pagination_class = CustomListPagination