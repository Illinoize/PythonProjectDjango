"""Importing model and serializers"""
from rest_framework import serializers  # pylint: disable=E0401
from wallets.models import Wallet  # pylint: disable=E0401
from django.contrib.auth.models import User  # pylint: disable=E0401


class WalletSerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=R0903
    """Create serialization for Wallet model"""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:  # pylint: disable=R0903
        """Create Meta class for model"""
        model = Wallet
        fields = ('url',
                  'id',
                  'owner',
                  'name',
                  'type',
                  'currency',
                  'balance',
                  'created_on',
                  'modified_on',)
        write_only_fields = ('owner',)
        read_only_fields = ('name', 'balance', 'created_on', 'modified_on',)


class UserSerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=R0903
    """Create serialization for User model"""
    wallets = serializers.HyperlinkedRelatedField(many=True, view_name='wallet-detail',
                                                  read_only=True)

    class Meta:  # pylint: disable=R0903
        """Create Meta class for User model"""
        model = User
        fields = ['url', 'id', 'username', 'wallets']
