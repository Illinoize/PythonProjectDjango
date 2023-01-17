"""Importing model and serializers"""
from rest_framework import serializers  # pylint: disable=E0401
from wallets.models import Wallet, Transaction  # pylint: disable=E0401
from django.contrib.auth.models import User  # pylint: disable=E0401
from django.utils.crypto import get_random_string # pylint: disable=E0401


class WalletSerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=R0903
    """Create serialization for Wallet model"""
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        """create wallet object"""
        obj = Wallet.objects.create(**validated_data)
        obj.name = get_random_string(length=8).upper()  # Name must consists of 8 symbols
        if obj.currency == 'RUB':
            obj.balance = format(100, '.2f')
        else:
            obj.balance = format(3, '.2f')
        obj.save()
        return obj

    class Meta:  # pylint: disable=R0903
        """Create Meta class for model"""
        model = Wallet
        fields = ['url',
                  'id',
                  'owner',
                  'name',
                  'type',
                  'currency',
                  'balance',
                  'created_on',
                  'modified_on',]
        read_only_fields = ('name', 'balance', 'created_on', 'modified_on',)


class UserSerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=R0903
    """Create serialization for User model"""
    wallets = serializers.HyperlinkedRelatedField(many=True, view_name='wallet-detail',
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
        fields = ['url', 'id', 'username', 'password', 'wallets']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):  # pylint: disable=R0903
    """Creating serialization for transaction"""
    sender = serializers.SlugRelatedField(slug_field='name', queryset=Wallet.objects.all())
    receiver = serializers.SlugRelatedField(slug_field='name', queryset=Wallet.objects.all())
    new_balance = serializers.SerializerMethodField()

    class Meta:  # pylint: disable=R0903
        """Creating Meta class for transactions"""
        model = Transaction
        fields = ['url', 'id', 'sender', 'receiver', 'transfer_amount',
                  'commission', 'status', 'timestamp', 'new_balance']
        read_only_fields = ('commission', 'status', 'timestamp')
        excluded_fields = ('new_balance',)

    def get_new_balance(self, sender, receiver, obj):
        """Changing balance"""
        receiver.balance += obj.transaction_amount
        sender.balance -= obj.transaction_amount
        receiver.save()
        sender.save()
        return sender, receiver

    def create(self, validated_data):
        """Creating transaction"""
        sender_wallet = Wallet.objects.all(**validated_data)
        receiver_wallet = Wallet.objects.all(**validated_data)
        if sender_wallet.currency == receiver_wallet.currency:
            self.get_new_balance(sender=sender_wallet,
                                 receiver=receiver_wallet, obj=Transaction.objects.all())
        else:
            raise ValueError('You cannot transfer money between wallets with different currency.')
