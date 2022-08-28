from rest_framework import serializers

from auth_app import models as AuthModels
from supplier import models as SupplierModels
from buyer import models as BuyerModels
from manager import models as ManagerModels
from payment import models as PaymentModels


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModels.User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "account_type",
            "is_active",
            "date_joined",
        )


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModels.Membership
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModels.ProductCategory
        fields = "__all__"


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModels.ProductSubCategory
        fields = "__all__"
        depth = 1


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModels.Store
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["products"] = (
            SupplierModels.Store.objects.filter(id=instance.id)
            .first()
            .store_product.all()
            .count()
        )
        return representation


class SuppliersSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AuthModels.ClientProfile
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["membership"] = PaymentModels.Membership.objects.filter(
            supplier=instance.user
        ).first()
        representation["stores"] = SupplierModels.Store.objects.filter(
            supplier=instance.user
        ).count()
        return representation


class BuyersSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AuthModels.ClientProfile
        fields = "__all__"


class _StoreSerializer(serializers.RelatedField, StoreSerializer):
    def to_internal_value(self, data):
        return self.queryset.get(name=data).pk

    def to_representation(self, value):
        return {"name": value.name, "slug": value.slug}


class ProductsSerializer(serializers.ModelSerializer):
    store = _StoreSerializer(queryset=SupplierModels.Store.objects.all(), many=True)
    sub_category = ProductSubCategorySerializer()

    class Meta:
        model = SupplierModels.Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["supplier"] = SuppliersSerializer(
            instance.store.all().first().supplier.profile
        ).data.get("business_name")
        representation["supplier_slug"] = SuppliersSerializer(
            instance.store.all().first().supplier.profile
        ).data.get("slug")
        representation["image"] = ProductImagesSerializer(
            SupplierModels.ProductImage.objects.filter(product=instance).first()
        ).data.get("image")
        return representation


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModels.ProductImage
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModels.Service
        fields = "__all__"


class ContractReciptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModels.ContractReceipt
        fields = "__all__"


class ContractsSerializer(serializers.ModelSerializer):
    supplier = UserSerializer()
    buyer = UserSerializer()
    service = ServiceSerializer()

    class Meta:
        model = PaymentModels.Contract
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["receipt"] = ContractReciptSerializer(
            PaymentModels.ContractReceipt.objects.filter(contract=instance).first()
        ).data
        return representation


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerModels.Location
        fields = "__all__"


class ManagerServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerModels.Service
        fields = "__all__"


class ShowroomsSerializer(serializers.ModelSerializer):
    location = LocationsSerializer()
    store = _StoreSerializer(queryset=SupplierModels.Store.objects.all(), many=True)

    class Meta:
        model = ManagerModels.Showroom
        fields = "__all__"

    def to_representation(self, instance):
        product_count = 0
        representation = super().to_representation(instance)
        for store in instance.store.all():
            product_count = product_count + store.store_product.all().count()

        representation["products"] = product_count
        return representation


class MembershipReciptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModels.MembershipReceipt
        fields = "__all__"


class MembershipSerializer(serializers.ModelSerializer):
    supplier = UserSerializer()

    class Meta:
        model = PaymentModels.Membership
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["receipt"] = MembershipReciptSerializer(
            PaymentModels.MembershipReceipt.objects.filter(membership=instance).first()
        ).data
        return representation
