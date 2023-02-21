# pylint: disable=consider-using-f-string  disable=import-error   disable=W0613
"""Importing modules"""
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.db.models import Q

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

    def perform_create(self, serializer: WalletSerializer):
        """Adding owner field for instances"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Get the list for authorised user"""
        user = self.request.user
        return Wallet.objects.filter(owner=user)


class UserViewSet(viewsets.ReadOnlyModelViewSet,  # pylint: disable=R0903
                  mixins.CreateModelMixin):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Get user transactions"""
        user = self.request.user
        return Transaction.objects.filter(Q(sender__owner=user) | Q(receiver__owner=user))

    def create(self, request, *args, **kwargs):
        """Create Transaction"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValueError:
            return Response("You do not have enough money or try to change money "
                            "between wallets with different currency",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
