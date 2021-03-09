from rest_framework import serializers


class CountUnusedAddressSerializer(serializers.Serializer):
    chain = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)


class ResetEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetEmailSerializer(serializers.Serializer):
    reset_email_key = serializers.CharField(required=True)
