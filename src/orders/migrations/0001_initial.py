# Generated by Django 4.0.2 on 2022-03-11 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=254)),
                ('type', models.CharField(choices=[('fixed', 'Fixed'), ('percentage', 'Percentage'), ('free_shipping', 'Free Shipping')], max_length=50)),
                ('is_valid', models.BooleanField(default=True)),
                ('amount', models.IntegerField()),
                ('active_from', models.CharField(max_length=100)),
                ('expire_at', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tracking_number', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('sales_tax', models.FloatField()),
                ('total', models.FloatField()),
                ('paid_total', models.FloatField()),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_gateway', models.CharField(choices=[('stripe', 'Stripe'), ('cod', 'COD')], default='cod', max_length=10)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('delivery_fee', models.FloatField(blank=True, null=True)),
                ('delivery_time', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderProductPivot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_quantity', models.IntegerField()),
                ('unit_price', models.IntegerField()),
                ('subtotal', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=254)),
                ('color', models.CharField(max_length=100)),
                ('serial', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
