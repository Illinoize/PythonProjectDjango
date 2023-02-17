# pylint: disable=import-error
"""Importing urls and views"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wallets import views


router = DefaultRouter()
router.register(r'wallets', views.WalletsViewSet, basename='wallet-list')
router.register(r'users', views.UserViewSet, basename='user')


urlpatterns = [
    path(r'wallets/transactions',
         views.TransactionViewSet.as_view({'post': 'create', 'get': 'list'})),
    path(r'wallets/transactions/<int:pk>', views.TransactionViewSet.as_view({'get': 'retrieve'})),
    path('', include(router.urls)),
]
