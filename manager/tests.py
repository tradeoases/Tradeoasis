from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

# apps
from manager import models
from supplier.models import Store
from auth_app.models import User


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
