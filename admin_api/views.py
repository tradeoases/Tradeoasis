from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
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
    queryset = AuthModels.ClientProfile.objects.filter(
        user__account_type="SUPPLIER"
    ).order_by("-id")
    serializer_class = serializers.SuppliersSerializer
    pagination_class = CustomListPagination


class SupplierRetrieveView(RetrieveAPIView):
    queryset = AuthModels.ClientProfile.objects.filter(
        user__account_type="SUPPLIER"
    ).order_by("-id")
    serializer_class = serializers.SuppliersSerializer
    lookup_field = "slug"


class BuyersListView(ListAPIView):
    queryset = AuthModels.ClientProfile.objects.filter(
        user__account_type="BUYER"
    ).order_by("-id")
    serializer_class = serializers.BuyersSerializer
    pagination_class = CustomListPagination


class BuyerRetrieveView(RetrieveAPIView):
    queryset = AuthModels.ClientProfile.objects.filter(
        user__account_type="BUYER"
    ).order_by("-id")
    serializer_class = serializers.BuyersSerializer
    lookup_field = "slug"


class ProductsListView(ListAPIView):
    queryset = SupplierModels.Product.objects.all().order_by("-id")
    serializer_class = serializers.ProductsSerializer
    pagination_class = CustomListPagination


class ProductRetrieveView(RetrieveAPIView):
    queryset = SupplierModels.Product.objects.all().order_by("-id")
    serializer_class = serializers.ProductsSerializer
    pagination_class = CustomListPagination
    lookup_field = "slug"


class ProductDeleteView(APIView):
    def post(self, request, slug):
        try:
            product = SupplierModels.Product.objects.filter(slug=slug)
            product.delete()

            # send mail

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SupplierProductsListView(ListAPIView):
    serializer_class = serializers.ProductsSerializer
    pagination_class = CustomListPagination
    lookup_field = "slug"

    def get_queryset(self):
        supplier = AuthModels.ClientProfile.objects.filter(
            slug=self.kwargs.get("slug")
        ).first()

        queryset = SupplierModels.Product.objects.filter(store__supplier=supplier.user)

        return queryset


class ProductImageListView(ListAPIView):
    serializer_class = serializers.ProductImagesSerializer
    pagination_class = CustomListPagination
    lookup_field = "slug"

    def get_queryset(self):
        product = SupplierModels.Product.objects.filter(
            slug=self.kwargs.get("slug")
        ).first()

        queryset = SupplierModels.ProductImage.objects.filter(
            product=product
        ).order_by()

        return queryset


class ContractsListView(ListAPIView):
    queryset = PaymentModels.Contract.objects.all().order_by("-id")
    serializer_class = serializers.ContractsSerializer
    pagination_class = CustomListPagination


class ContractRetrieveView(RetrieveAPIView):
    queryset = PaymentModels.Contract.objects.all().order_by("-id")
    serializer_class = serializers.ContractsSerializer
    pagination_class = CustomListPagination
    lookup_field = "id"


class ShowroowListView(ListAPIView):
    queryset = ManagerModels.Showroom.objects.all().order_by("-id")
    serializer_class = serializers.ShowroomsSerializer
    pagination_class = CustomListPagination


class ShowroowRetrieveView(RetrieveAPIView):
    queryset = ManagerModels.Showroom.objects.all().order_by("-id")
    serializer_class = serializers.ShowroomsSerializer
    pagination_class = CustomListPagination
    lookup_field = "slug"


class SupplierShowroowListView(ListAPIView):
    queryset = ManagerModels.Showroom.objects.all().order_by("-id")
    serializer_class = serializers.ShowroomsSerializer

    def get_queryset(self):
        supplier = AuthModels.ClientProfile.objects.filter(
            slug=self.kwargs.get("slug")
        ).first()

        queryset = ManagerModels.Showroom.objects.filter(
            store__in=supplier.user.store_set.all().order_by("-id")
        )

        return queryset


class ManagerServicesListView(ListAPIView):
    queryset = ManagerModels.Service.objects.all().order_by("-id")
    serializer_class = serializers.ManagerServicesSerializer
    pagination_class = CustomListPagination


class ManagerServiceRetrieveView(RetrieveAPIView):
    queryset = ManagerModels.Service.objects.all().order_by("-id")
    serializer_class = serializers.ManagerServicesSerializer
    pagination_class = CustomListPagination
    lookup_field = "slug"


class MembershipListView(ListAPIView):
    queryset = PaymentModels.Membership.objects.all().order_by("-id")
    serializer_class = serializers.MembershipSerializer
    pagination_class = CustomListPagination


class StoreListView(ListAPIView):
    queryset = SupplierModels.Store.objects.all().order_by("-id")
    serializer_class = serializers.StoreSerializer
    pagination_class = CustomListPagination


class StoreRetrieveView(RetrieveAPIView):
    queryset = SupplierModels.Store.objects.all().order_by("-id")
    serializer_class = serializers.StoreSerializer
    pagination_class = CustomListPagination
    lookup_field = "slug"


class SupplierStoresListView(ListAPIView):
    queryset = SupplierModels.Store.objects.all().order_by("-id")
    serializer_class = serializers.StoreSerializer
    pagination_class = CustomListPagination

    def get_queryset(self):
        supplier = AuthModels.ClientProfile.objects.filter(
            slug=self.kwargs.get("slug")
        ).first()

        queryset = SupplierModels.Store.objects.filter(supplier=supplier.user)

        return queryset


class ServicesListView(ListAPIView):
    queryset = ManagerModels.Service.objects.all().order_by("-id")
    serializer_class = serializers.ManagerServicesSerializer
    pagination_class = CustomListPagination


class ServiceRetrieveView(RetrieveAPIView):
    queryset = ManagerModels.Service.objects.all().order_by("-id")
    serializer_class = serializers.ManagerServicesSerializer
    pagination_class = CustomListPagination
    lookup_field = "slug"


class SuspendAccountView(APIView):
    def post(self, request, slug):
        try:
            user = AuthModels.ClientProfile.objects.filter(slug=slug).first().user

            # not working
            user.is_active = False
            user.save()

            # send mail
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
