from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

# from apps
from supplier import models
from auth_app.models import Supplier


class SupplierTest(TestCase):
    def test_models_created(self):
        # supplier
        test_supplier = Supplier.objects.create(
            username="testuser", email="test@test.com", password="testUser123"
        )

        # store can exist in one location
        test_store = models.Store.objects.create(
            name="test store name", supplier=test_supplier
        )

        # test_store.location.add(test_location)
        # self.assertIn(test_store, models.Store.objects.filter(location=test_location))

        # product category
        test_category = models.ProductCategory.objects.create(
            name="Fashion",
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open(
                    f"{settings.STATICFILES_DIRS[0]}/images/test/django.png", "rb"
                ).read(),
                content_type="image/png",
            ),
        )

        test_product = models.Product.objects.create(
            name="product name",
            description="product description",
            category=test_category,
            price="200.0",
            currency="USD",
        )

        # category product count increases
        self.assertEqual(test_category.product_count, 1)

        test_product.store.add(test_store)
        self.assertIn(test_product, models.Product.objects.filter(store=test_store))

        # add images
        test_product_image = models.ProductImage(
            product=test_product,
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open(
                    f"{settings.STATICFILES_DIRS[0]}/images/test/django.png", "rb"
                ).read(),
                content_type="image/png",
            ),
        )
        test_product_image.save()

        # suppliers can create services, on which buyer can make contracts
        test_supplier_service = models.Service.objects.create(
            supplier=test_supplier,
            name="Represention",
            description="Test description",
            price="200.0",
            currency="USD",
        )

        # confirm product images are deleted
        test_product.delete()
        self.assertFalse(models.ProductImage.objects.filter(id=test_product_image.id))
