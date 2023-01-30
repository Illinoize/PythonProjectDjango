# pylint: disable=import-error
"""Importing model and serializers"""
from rest_framework import serializers
from django.contrib.auth.models import User

from wallets.models import Wallet, Transaction


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
        read_only_fields = ['name', 'balance', 'created_on', 'modified_on']

    def update(self, instance, validated_data):
        """Update Wallet serializer"""
        instance.balance = validated_data.get('balance', instance.email)
        instance.modified_on = validated_data.get('modified_on', instance.content)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):  # pylint: disable=R0903
    """Create serialization for User model"""
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
    sender = serializers.SlugRelatedField(queryset=Wallet.objects.all(), slug_field='name')
    receiver = serializers.SlugRelatedField(queryset=Wallet.objects.all(), slug_field='name')

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
        read_only_fields = ['commission', 'status', 'timestamp']
