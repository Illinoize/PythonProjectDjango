# pylint: disable=consider-using-f-string  disable=import-error
"""Importing render"""
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.auth.models import User
from wallets.models import Wallet
from wallets.serializers import WalletSerializer, UserSerializer
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


class UserList(viewsets.ReadOnlyModelViewSet):  # pylint: disable=R0903
    """Creating user list"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class CreateTransaction(generics.CreateAPIView):  # pylint: disable=R0903
#     """Creating Transaction"""
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
# class WalletTransaction(generics.ListAPIView):  # pylint: disable=R0903
#     """Get a list where wallet is sender or receiver"""
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
#
#
# class UserTransaction(generics.ListAPIView):  # pylint: disable=R0903
#     """Get all transactions from user"""
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
#
#
# class TransactionDetail(generics.RetrieveAPIView):  # pylint: disable=R0903
#     """Get information about one transaction"""
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
