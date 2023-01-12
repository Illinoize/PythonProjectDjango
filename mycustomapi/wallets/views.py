# pylint: disable=consider-using-f-string
"""Importing render"""
from rest_framework import mixins  # pylint: disable=E0401
from rest_framework import generics  # pylint: disable=E0401

from wallets.models import Wallet  # pylint: disable=E0401
from wallets.serializers import WalletSerializer  # pylint: disable=E0401


class WalletList(mixins.ListModelMixin,
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

# @api_view(['GET', 'POST', 'DELETE'])
# def wallet_list(request):  # pylint: disable=R1710
#     """Creating and deleting wallets or getting info about wallets"""
#     if request.method == 'GET':
#         wallets = Wallet.objects.all()
#         name = request.query_params.get('name', None)
#         if name is not None:
#             wallets = wallets.filter(title__icontains=name)
#         wallets_serializer = WalletSerializer(wallets, many=True)
#         return JsonResponse(wallets_serializer.data, safe=False)
#
#     if request.method == 'POST':
#         wallet_serializer = WalletSerializer(data=request.data)
#         if wallet_serializer.is_valid():
#             wallet_serializer.save()
#             return JsonResponse(wallet_serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(wallet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         count = Wallet.objects.all().delete()
#         return JsonResponse({'message': '{} Wallet were deleted successfully!'.format(count[0])},
#                             status=status.HTTP_204_NO_CONTENT)
