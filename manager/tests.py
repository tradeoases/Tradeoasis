from ast import arg
from itertools import product
from unicodedata import category
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.urls import resolve, reverse_lazy

# apps
from manager import models
from supplier.models import Store, Product, ProductCategory
from auth_app.models import User

from manager import views


class ModelTest(TestCase):
    def test_models_created(self):
        # locations
        location_test = models.Location(
            name="UAE - Dubai",
        )

        location_test.save()

        # Service
        service_test = models.Service(
            name="Represention", description="Test description"
        )

        service_test.save()

        # service images

        # confirm mediaroot is set
        self.assertTrue(settings.MEDIA_URL)
        self.assertTrue(settings.MEDIA_ROOT)

        service_img_test = models.ServiceImage(
            service=service_test,
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open(
                    f"{settings.STATICFILES_DIRS[0]}/images/test/django.png", "rb"
                ).read(),
                content_type="image/png",
            ),
        )
        service_img_test.save()

        # showrooms

        test_supplier = User.objects.create(
            username="testuser", email="test@test.com", password="testUser123"
        )

        test_store = Store.objects.create(
            name="test store name", supplier=test_supplier
        )

        showroom_test = models.Showroom.objects.create(
            location=location_test,
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=open(
                    f"{settings.STATICFILES_DIRS[0]}/images/test/django.png", "rb"
                ).read(),
                content_type="image/png",
            ),
            visits=10,
        )

        # store can exist in multiple showroows

        showroom_test.store.add(test_store)
        self.assertIn(showroom_test, models.Showroom.objects.filter(store=test_store))


class RequestTest(TestCase):
    fixtures = ['supplier.json','profile.json','store.json','category.json', 'products.json']

    def setUp(self):
        self.client = Client()
        return super().setUp()

    def test_app_urls(self):
        response = self.client.get("")
        # home
        home_found = resolve("/")
        self.assertEqual(home_found.func.__name__, views.HomeView.as_view().__name__)

        # Products
        products_found = resolve("/products/")
        self.assertEqual(
            products_found.func.__name__, views.ProductListView.as_view().__name__
        )

        # Product detail
        products_found = resolve(f"/products/test_slug")
        self.assertEqual(
            products_found.func.__name__, views.ProductDetailView.as_view().__name__
        )

        # # showrooms
        # products_found = resolve("/showrooms/")
        # self.assertEqual(products_found.func.__name__, views.ProductListView.as_view().__name__)

        # # services
        # products_found = resolve("/services/")
        # self.assertEqual(products_found.func.__name__, views.ProductListView.as_view().__name__)

        # # support
        # products_found = resolve("/support/")
        # self.assertEqual(products_found.func.__name__, views.ProductListView.as_view().__name__)

        # # about-us
        # products_found = resolve("/about-us/")
        # self.assertEqual(products_found.func.__name__, views.ProductListView.as_view().__name__)

    def test_home_page(self):
        # a request is made to that base app
        response = self.client.get("")

        # template used
        self.assertTemplateUsed(response, "manager/home.html")

        # view context
        home_view_context = [
            "view_name",
            "product_categories",
            "showrooms",
            "stores",
            "catogory_product_group",
            "new_arrivals",
        ]
        
        for context_name in home_view_context:
            self.assertIn(context_name, response.context)

    # def test_product_list_page(self):

    #     product = Product.objects.all().first()
    #     # a request is made to that base app
    #     response = self.client.get("/products/")

    #     # template used
    #     self.assertTemplateUsed(response, "supplier/product_list.html")

    #     # view context
    #     home_view_context = ["view_name", "product_categories", "product_list"]

    #     for context_name in home_view_context:
    #         self.assertIn(context_name, response.context)

    #     self.assertIn(product, response.context.get('object_list'))

    # def test_product_detail_page(self):

    #     product = Product.objects.all().first()

    #     # a request is made to that base app
    #     response = self.client.get(reverse_lazy('manager:product-detail', args=[product.slug]))
    #     self.assertEqual(response.status_code, 200)

    #     # # template used
    #     self.assertTemplateUsed(response, "supplier/product_detail.html")

    #     # # view context
    #     home_view_context = ['view_name', 'product_categories', 'product', 'related_products', 'product_images']

    #     for context_name in home_view_context:
    #         self.assertIn(context_name, response.context)

    #     self.assertAlmostEquals(response.context.get('product').name, product.name)


    # def test_category_list_view(self):

    #     category = ProductCategory.objects.all().first()
    #     # a request is made to that base app
    #     response = self.client.get("/categories/")

    #     # template used
    #     self.assertTemplateUsed(response, "supplier/productcategory_list.html")

    #     # view context
    #     # home_view_context = ["view_name", "product_categories", "product_list"]

    #     # for context_name in home_view_context:
    #     #     self.assertIn(context_name, response.context)

    #     # self.assertIn(product, response.context.get('object_list'))
        
    # def test_category_detail_view(self):
    #     category = ProductCategory.objects.all().first()

    #     # a request is made to that base app
    #     response = self.client.get(reverse_lazy('manager:category-detail', args=[category.slug]))
    #     self.assertEqual(response.status_code, 200)

    #     # # template used
    #     self.assertTemplateUsed(response, "supplier/productcategory_detail.html")

    #     # # view context
    #     home_view_context = ['view_name', 'products', 'product_count', 'other_categories']

    #     for context_name in home_view_context:
    #         self.assertIn(context_name, response.context)

    #     self.assertAlmostEquals(response.context.get('productcategory').name, category.name)
