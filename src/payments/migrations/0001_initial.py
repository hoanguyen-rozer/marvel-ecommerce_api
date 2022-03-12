# Generated by Django 4.0.2 on 2022-03-11 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('expiry_month', models.CharField(max_length=50)),
                ('expiry_year', models.CharField(max_length=50)),
                ('cvv', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField()),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('on_hold', 'On hold'), ('rejected', 'Rejected'), ('processing', 'Processing')], max_length=15)),
                ('payment_method', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=254)),
                ('note', models.CharField(max_length=100)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]