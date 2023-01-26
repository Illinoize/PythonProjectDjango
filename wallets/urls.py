# pylint: disable=import-error
"""Importing urls and views"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wallets import views


router = DefaultRouter()
router.register(r'wallets', views.WalletsViewSet, basename='wallet-list')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')


urlpatterns = [
    path('', include(router.urls)),
]
