# pylint: disable=import-error
"""Importing model and serializers"""
from rest_framework import serializers
from wallets.models import Wallet, Transaction
from django.contrib.auth.models import User


class WalletSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """Create serialization for Wallet model"""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:  # pylint: disable=R0903
        """Create Meta class for model"""
        model = Wallet
        fields = ['id',
                  'owner',
                  'name',
                  'type',
                  'currency',
                  'balance',
                  'created_on',
                  'modified_on']
        read_only_fields = ['name', 'balance', 'created_on', 'modified_on',]


class UserSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """Create serialization for User model"""
    wallets = serializers.HyperlinkedRelatedField(many=True, view_name='wallet-name',
                                                  read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Create user"""
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:  # pylint: disable=R0903
        """Create Meta class for User model"""
        model = User
        fields = ['id', 'username', 'password', 'wallets']


class TransactionSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """Create serialization for transactions"""
    class Meta:  # pylint: disable=R0903
        """Create Meta class for Transaction model"""
        model = Transaction
        fields = ['id',
                  'sender',
                  'receiver',
                  'transfer_amount',
                  'commission',
                  'status',
                  'timestamp']
        read_only_fields = ['commission', 'status']
