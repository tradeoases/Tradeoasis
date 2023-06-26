# Generated by Django 4.2.2 on 2023-06-26 14:38

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_app', '0001_initial'),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BraintreeSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='current_billing_cycle')),
                ('payment_method', models.CharField(blank=True, max_length=20, null=True, verbose_name='Payment Method')),
                ('current_billing_cycle', models.CharField(blank=True, max_length=256, null=True, verbose_name='current_billing_cycle')),
                ('days_past_due', models.CharField(blank=True, max_length=256, null=True, verbose_name='days_past_due')),
                ('next_billing_date', models.CharField(blank=True, max_length=256, null=True, verbose_name='next_billing_date')),
                ('payment_method_token', models.CharField(blank=True, max_length=256, null=True, verbose_name='payment_method_token')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Reference Number')),
                ('is_complete', models.BooleanField(default=False, verbose_name='Contract completed')),
                ('is_accepted', models.BooleanField(default=False, verbose_name='Contract accepted')),
                ('payment_made', models.BooleanField(default=False, verbose_name='Contract payment made')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='auth_app.buyer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_service', to='supplier.service')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='auth_app.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='id')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('name_ar', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('name_fr', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('name_de', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('name_en', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('price', models.CharField(blank=True, max_length=256, null=True, verbose_name='price')),
                ('price_ar', models.CharField(blank=True, max_length=256, null=True, verbose_name='price')),
                ('price_fr', models.CharField(blank=True, max_length=256, null=True, verbose_name='price')),
                ('price_de', models.CharField(blank=True, max_length=256, null=True, verbose_name='price')),
                ('price_en', models.CharField(blank=True, max_length=256, null=True, verbose_name='price')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='description')),
                ('billing_frequency', models.CharField(blank=True, max_length=256, null=True, verbose_name='billing_frequency')),
                ('currency_iso_code', models.CharField(blank=True, max_length=256, null=True, verbose_name='Currency')),
                ('currency_iso_code_ar', models.CharField(blank=True, max_length=256, null=True, verbose_name='Currency')),
                ('currency_iso_code_fr', models.CharField(blank=True, max_length=256, null=True, verbose_name='Currency')),
                ('currency_iso_code_de', models.CharField(blank=True, max_length=256, null=True, verbose_name='Currency')),
                ('currency_iso_code_en', models.CharField(blank=True, max_length=256, null=True, verbose_name='Currency')),
                ('interval_unit', models.CharField(max_length=256, verbose_name='Duration')),
                ('status', models.CharField(max_length=256, verbose_name='Status')),
                ('has_trial', models.BooleanField(default=False, verbose_name='Has Trial Period')),
                ('trial_period', models.CharField(blank=True, max_length=256, null=True, verbose_name='Trial Period')),
                ('trial_period_count', models.CharField(blank=True, max_length=256, null=True, verbose_name='Trial Period Count')),
                ('paypal_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='paypal_id')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.CharField(blank=True, choices=[('BRAINTREE CARD', 'BRAINTREE CARD'), ('PAYPAL', 'PAYPAL')], max_length=256, null=True, verbose_name='Type')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Subscription Start Date')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='Subscription Expiry Date')),
                ('status', models.BooleanField(default=False, verbose_name='Active')),
                ('payment_completed', models.BooleanField(default=False, verbose_name='Payment Completed')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_app.supplier')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature', to='payment.feature')),
                ('previous_feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_pricing', to='payment.feature')),
                ('upgrading_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upgrading_to', to='payment.feature')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('name_ar', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('name_fr', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('name_de', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('name_en', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_ar', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_de', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModeOfPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('transaction_count', models.IntegerField(default=0, verbose_name='Number of transactions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaypalProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='Product Id')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('ProductType', models.CharField(default='Service', max_length=256, verbose_name='Type')),
                ('description', models.TextField(max_length=256, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='PaypalSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_key', models.CharField(blank=True, max_length=256, null=True, verbose_name='Order key')),
                ('created_on', models.DateField(default=datetime.date.today, verbose_name='Created on')),
                ('membership', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paypal_membership', to='payment.membership')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=20, verbose_name='Payment Method')),
                ('plan_id', models.CharField(max_length=30, verbose_name='Plan Id')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('name_ar', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('name_fr', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('name_de', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('name_en', models.CharField(max_length=256, null=True, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_ar', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_de', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('features', models.ManyToManyField(related_name='features_list', to='payment.feature')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.membershipgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContractReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=256, verbose_name='Address')),
                ('payment_id', models.CharField(max_length=256, verbose_name='Payment Id')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Total Amount Paid')),
                ('currency', models.CharField(max_length=6, verbose_name='Currency')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.contract')),
                ('mode_of_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.modeofpayment')),
            ],
        ),
        migrations.CreateModel(
            name='CardPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_token', models.CharField(max_length=256, verbose_name='card_token')),
                ('card_last_4', models.CharField(max_length=256, verbose_name='card_last_4')),
                ('card_type', models.CharField(max_length=256, verbose_name='card_type')),
                ('card_expiration_month', models.CharField(max_length=256, verbose_name='card_expiration_month')),
                ('card_expiration_year', models.CharField(max_length=256, verbose_name='card_expiration_year')),
                ('card_customer_location', models.CharField(max_length=256, verbose_name='card_customer_location')),
                ('card_issuing_bank', models.CharField(max_length=256, verbose_name='card_issuing_bank')),
                ('subscription', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payment.braintreesubscription')),
            ],
        ),
        migrations.AddField(
            model_name='braintreesubscription',
            name='membership',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='braintree_membership', to='payment.membership'),
        ),
    ]
