from rest_framework import serializers


class CountUnusedAddressSerializer(serializers.Serializer):
    chain = serializers.CharField(required=True)


class AddDepositAddressSerializer(serializers.Serializer):
    chain = serializers.CharField(required=True)
    addr_list = serializers.ListField(required=True)


class DepositNotifySerializer(serializers.Serializer):
    token_id = serializers.CharField(required=True)
    where_from = serializers.CharField(required=True)
    to = serializers.CharField(required=True)
    memo = serializers.CharField(required=False)
    amount = serializers.CharField(required=True)
    tx_hash = serializers.CharField(required=True)
    index = serializers.CharField(required=True)
    block_height = serializers.CharField(required=True)
    block_time = serializers.CharField(required=True)


class ResetEmailSerializer(serializers.Serializer):
    reset_email_key = serializers.CharField(required=True)


class SuccessfulWithdrawalNotifySerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True)
    token_id = serializers.CharField(required=True)
    to = serializers.CharField(required=True)
    memo = serializers.CharField(required=False)
    amount = serializers.CharField(required=True)
    tx_hash = serializers.CharField(required=True)
    block_height = serializers.CharField(required=True)
    block_time = serializers.CharField(required=True)
    