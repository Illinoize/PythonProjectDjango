"""Importing urls and views"""
from django.urls import path  # pylint: disable=E0401
from wallets import views  # pylint: disable=E0401

urlpatterns = [
    path('', views.api_root),
    path('wallets/', views.WalletsList.as_view(), name='wallet-list'),
    path('wallets/<int:pk>/', views.WalletName.as_view(), name='wallet-detail'),
]
