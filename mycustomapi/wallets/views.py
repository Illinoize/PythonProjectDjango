# pylint: disable=consider-using-f-string
"""Importing render"""
from django.shortcuts import render  # pylint: disable=E0401 disable=W0611

from django.http.response import JsonResponse  # pylint: disable=E0401
from rest_framework.parsers import JSONParser  # pylint: disable=E0401 disable=W0611
from rest_framework import status  # pylint: disable=E0401

from wallets.models import Wallet  # pylint: disable=E0401
from wallets.serializers import WalletSerializer  # pylint: disable=E0401
from rest_framework.decorators import api_view  # pylint: disable=E0401 disable=C0412


@api_view(['GET', 'POST', 'DELETE'])
def wallet_list(request):  # pylint: disable=R1710
    """Creating and deleting wallets or getting info about wallets"""
    if request.method == 'GET':
        wallets = Wallet.objects.all()
        name = request.query_params.get('name', None)
        if name is not None:
            wallets = wallets.filter(title__icontains=name)
        wallets_serializer = WalletSerializer(wallets, many=True)
        return JsonResponse(wallets_serializer.data, safe=False)

    if request.method == 'POST':
        wallet_serializer = WalletSerializer(data=request.data)
        if wallet_serializer.is_valid():
            wallet_serializer.save()
            return JsonResponse(wallet_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(wallet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        count = Wallet.objects.all().delete()
        return JsonResponse({'message': '{} Wallet were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)
