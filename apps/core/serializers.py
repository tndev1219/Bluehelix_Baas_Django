from rest_framework import serializers


class CountUnusedAddressSerializer(serializers.Serializer):
    chain = serializers.CharField(required=True)


class AddDepositAddressSerializer(serializers.Serializer):
    chain = serializers.CharField(required=True)
    addr_list = serializers.ListField(required=True)


class ResetEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetEmailSerializer(serializers.Serializer):
    reset_email_key = serializers.CharField(required=True)
