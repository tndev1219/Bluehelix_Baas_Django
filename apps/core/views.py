import time
import requests
import ed25519
import json
from binascii import hexlify, unhexlify
from django.http import JsonResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from apps.core.serializers import CountUnusedAddressSerializer, AddDepositAddressSerializer
from apps.core.utils import create_sign_msg


class BaasViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'], serializer_class=CountUnusedAddressSerializer, url_path='count-unused-address')
    def count_unused_address(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            timestamp = str(int(time.time() * 1000))
            path = "/api/v1/address/unused/count?chain=" + serializer.validated_data['chain']

            sign_msg = create_sign_msg("GET", path, timestamp, {})
            sign_msg = sign_msg.encode("utf-8")

            signing_key = ed25519.SigningKey(settings.PRIVATE_KEY.encode("utf-8"), encoding="hex")
            signature = signing_key.sign(sign_msg)
            print("signature = ", hexlify(signature))

            headers  = {
                "BWAAS-API-KEY": settings.API_KEY,
                "BWAAS-API-TIMESTAMP": timestamp,
                "BWAAS-API-SIGNATURE": hexlify(signature)
            }

            try:
                res = requests.get(url=settings.DOMAIN+path, headers=headers)
                return JsonResponse({
                    'success': True,
                    'message': 'Success',
                    'result': res.text
                }, status=status.HTTP_200_OK)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Error Occured!',
                    'result': ValueError
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Count the Number of Unused Address Error: ', e)
            return JsonResponse({
                'success': False,
                'message': serializer.errors,
                'result': []
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], serializer_class=AddDepositAddressSerializer, url_path='add-deposit-address')
    def add_deposit_address(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            timestamp = str(int(time.time() * 1000))

            data = {
                "chain": serializer.validated_data['chain'],
                "addr_list": serializer.validated_data['addr_list']
            }
            sign_msg = create_sign_msg(
                "POST", "/api/v1/address/add", timestamp, data)
            sign_msg = sign_msg.encode("utf-8")

            signing_key = ed25519.SigningKey(settings.PRIVATE_KEY.encode("utf-8"), encoding="hex")
            signature = signing_key.sign(sign_msg)
            print("signature = ", hexlify(signature))

            headers = {
                "BWAAS-API-KEY": settings.API_KEY,
                "BWAAS-API-TIMESTAMP": timestamp,
                "BWAAS-API-SIGNATURE": hexlify(signature),
                "Content-Type": "application/json"
            }

            try:
                res = requests.post(url=settings.DOMAIN+"/api/v1/address/add", data=json.dumps(data),  headers=headers)
                return JsonResponse(
                {
                    'success': True,
                    'message': 'Success',
                    'result': res.text,
                }, status=status.HTTP_200_OK)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Error Occured!',
                    'result': ValueError
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Add Deposit Address Error: ', e)
            return JsonResponse({
                'success': False,
                'message': serializer.errors,
                'result': []
            }, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['PATCH'], serializer_class=UserSerializer, permission_classes=[IsAuthenticated], url_path='update-profile/(?P<pk>[0-9]+)')
    # def update_profile(self, request, *args, **kwargs):
    #     try:
    #         user = get_user_model().objects.filter(id=kwargs['pk'])
    #         if user:
    #             partial = kwargs.pop('partial', True)
    #             instance = self.get_object()
    #             serializer = self.serializer_class(instance, data=request.data, partial=partial)
    #             serializer.is_valid(raise_exception=True)
    #             serializer.save()

    #             return JsonResponse({
    #                 'success': True,
    #                 'message': 'Success',
    #                 'result': serializer.data
    #             }, status=status.HTTP_200_OK)
    #         else:
    #             return JsonResponse({
    #                 'success': False,
    #                 'message': 'User Not Found',
    #                 'result': []
    #             }, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         print('Update Profile Error: ', e)
    #         return JsonResponse({
    #             'success': False,
    #             'message': serializer.errors,
    #             'result': []
    #         }, status=status.HTTP_400_BAD_REQUEST)
