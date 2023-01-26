# pylint: disable=consider-using-f-string  disable=import-error
"""Importing render"""
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.auth.models import User
from wallets.models import Wallet, Transaction
from wallets.serializers import WalletSerializer, UserSerializer, TransactionSerializer
from wallets.permissions import IsOwnerOrReadOnly


class WalletsViewSet(viewsets.GenericViewSet,  # pylint: disable=R0903
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    """Creating views of wallets"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Adding owner field for instances"""
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # pylint: disable=R0903
    """Creating user list"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(viewsets.GenericViewSet,  # pylint: disable=R0903
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin):
    """Creating/Receiving a transaction"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
