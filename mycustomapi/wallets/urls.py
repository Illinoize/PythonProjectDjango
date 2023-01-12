"""Importing urls and views"""
from django.urls import path # pylint: disable=E0401
from wallets import views # pylint: disable=E0401

urlpatterns = [
    path('wallets/', views.wallets_list),
    path('wallets/name/', views.wallet_details),
]
