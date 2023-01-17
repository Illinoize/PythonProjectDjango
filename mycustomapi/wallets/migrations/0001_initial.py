# Generated by Django 4.1.5 on 2023-01-17 09:39
# pylint: disable=import-error disable=invalid-name  disable=too-few-public-methods
# pylint: disable=missing-module-docstring disable=missing-class-docstring

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_amount', models.FloatField(default=0)),
                ('commission', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('PAID', 'PAID'),
                                                     ('FAILED', 'FAILED')],
                                            default='PAID', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=8)),
                ('type', models.CharField(choices=[('Visa', 'Visa'),
                                                   ('Mastercard', 'Mastercard')],
                                          default='Visa', max_length=100)),
                ('currency', models.CharField(choices=[('USD', 'USD'),
                                                       ('RUB', 'RUB'),
                                                       ('EUR', 'EUR')],
                                              default='USD', max_length=100)),
                ('balance', models.FloatField(default=0)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('modified_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='wallets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
