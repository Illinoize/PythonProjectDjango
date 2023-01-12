"""Importing urls and views"""
from django.urls import path  # pylint: disable=E0401
from wallets import views  # pylint: disable=E0401
from rest_framework.urlpatterns import format_suffix_patterns  # pylint: disable=E0401

urlpatterns = [
    path('wallets/', views.WalletList.as_view()),
    path('wallets/name/', views.WalletName.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
