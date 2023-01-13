# pylint: disable=consider-using-f-string
"""Importing render"""
from rest_framework import mixins  # pylint: disable=E0401
from rest_framework import generics  # pylint: disable=E0401
from rest_framework import permissions  # pylint: disable=E0401
from rest_framework.decorators import api_view  # pylint: disable=E0401
from rest_framework.response import Response  # pylint: disable=E0401
from rest_framework.reverse import reverse  # pylint: disable=E0401
from django.contrib.auth.models import User  # pylint: disable=E0401
from wallets.models import Wallet  # pylint: disable=E0401
from wallets.serializers import WalletSerializer, UserSerializer  # pylint: disable=E0401
from wallets.permissions import IsOwnerOrReadOnly  # pylint: disable=E0401


@api_view(['GET'])
def api_root(request):
    """Creating root for urls"""
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'wallets': reverse('wallet-list', request=request, format=format)
    })


class WalletsList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """Creating views of wallets"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """Adding owner field for instances"""
        serializer.save(owner=self.request.user)

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        """Get a wallet info"""
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete a wallet"""
        return self.destroy(request, *args, **kwargs)


class UserList(generics.ListAPIView):  # pylint: disable=R0903
    """Getting list of users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):  # pylint: disable=R0903
    """Getting info about user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
