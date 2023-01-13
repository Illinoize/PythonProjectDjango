"""Importing model and serializers"""
from rest_framework import serializers  # pylint: disable=E0401
from wallets.models import Wallet  # pylint: disable=E0401
from django.contrib.auth.models import User  # pylint: disable=E0401


class WalletSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """Create serialization for Wallet model"""
    class Meta:  # pylint: disable=R0903
        """Create Meta class for model"""
        owner = serializers.ReadOnlyField(source='owner.username')
        model = Wallet
        fields = ('id',
                  'owner'
                  'name',
                  'type',
                  'currency',
                  'balance',
                  'created_on',
                  'modified_on',)
        read_only_fields = ('name', 'balance', 'created_on', 'modified_on',)


class UserSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """Create serialization for User model"""
    wallets = serializers.PrimaryKeyRelatedField(many=True, queryset=Wallet.objects.all())

    class Meta:  # pylint: disable=R0903
        """Create Meta class for User model"""
        model = User
        fields = ['id', 'username', 'wallets']
