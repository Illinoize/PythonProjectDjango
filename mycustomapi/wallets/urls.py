"""Importing urls and views"""
from django.urls import path  # pylint: disable=E0401
from wallets import views  # pylint: disable=E0401

urlpatterns = [
    path('wallets/', views.WalletsList.as_view()),
    path('wallets/<int:pk>/', views.WalletName.as_view()),
]
