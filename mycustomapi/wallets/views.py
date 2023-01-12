# pylint: disable=consider-using-f-string
"""Importing render"""
from rest_framework import mixins  # pylint: disable=E0401
from rest_framework import generics  # pylint: disable=E0401

from wallets.models import Wallet  # pylint: disable=E0401
from wallets.serializers import WalletSerializer  # pylint: disable=E0401


class WalletsList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """Creating views of wallets"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get(self, request, *args, **kwargs):
        """Get list of objects"""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create an object"""
        return self.create(request, *args, **kwargs)


class WalletName(mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """Working with wallets"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get(self, request, *args, **kwargs):
        """Get a wallet info"""
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete a wallet"""
        return self.destroy(request, *args, **kwargs)
