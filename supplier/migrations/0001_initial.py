# Generated by Django 4.0.6 on 2022-08-18 12:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import supplier.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='Price')),
                ('currency', models.CharField(max_length=6, verbose_name='Currency')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('product_count', models.IntegerField(default=0, verbose_name='Number of products')),
                ('image', models.ImageField(default='test/django.png', upload_to=supplier.models.get_file_path, verbose_name='Image')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Store Name')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('image', models.ImageField(default='test/django.png', upload_to=supplier.models.get_file_path, verbose_name='Service Image')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=3, max_digits=122, verbose_name='Price')),
                ('currency', models.CharField(max_length=6, verbose_name='Currency')),
                ('contract_count', models.IntegerField(default=0, verbose_name='Number of contracts')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('image', models.ImageField(default='test/django.png', upload_to=supplier.models.get_file_path, verbose_name='Image')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=supplier.models.get_file_path, verbose_name='Image')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supplier.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ManyToManyField(related_name='store_product', to='supplier.store'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.productsubcategory'),
        ),
    ]
