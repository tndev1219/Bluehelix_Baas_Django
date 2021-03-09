import time
import requests
import ed25519
import json
from binascii import hexlify, unhexlify
from django.http import JsonResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from apps.core.serializers import CountUnusedAddressSerializer, AddDepositAddressSerializer, DepositNotifySerializer
from apps.core.utils import create_sign_msg


class BaasViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'], url_path='create-keys')
    def create_keys(self, request, *args, **kwargs):
        try:
            signing_key, verifying_key = ed25519.create_keypair()
            return JsonResponse({
                'success': True,
                'message': 'Success',
                'result': {
                    "private_key" : str(signing_key.to_ascii(encoding="hex")),
                    "public_key": str(verifying_key.to_ascii(encoding="hex"))
                }
            }, status=status.HTTP_200_OK)
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Error Occured!',
                'result': ValueError
            }, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['POST'], serializer_class=DepositNotifySerializer, url_path='deposit-notify')
    def deposit_notify(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            timestamp = str(int(time.time() * 1000))

            data = {
                "token_id": serializer.validated_data['token_id'],
                "from": serializer.validated_data['where_from'],
                "to": serializer.validated_data['to'],
                "amount": serializer.validated_data['amount'],
                "tx_hash": serializer.validated_data['tx_hash'],
                "index": serializer.validated_data['index'],
                "block_height": serializer.validated_data['block_height'],
                "block_time": serializer.validated_data['block_time'],
            }
            if 'memo' in serializer.validated_data:
                data['memo'] = serializer.validated_data['memo']

            sign_msg = create_sign_msg(
                "POST", "/api/v1/notify/deposit", timestamp, data)
            sign_msg = sign_msg.encode("utf-8")

            signing_key = ed25519.SigningKey(settings.PRIVATE_KEY.encode("utf-8"), encoding="hex")
            signature = signing_key.sign(sign_msg)

            headers = {
                "BWAAS-API-KEY": settings.API_KEY,
                "BWAAS-API-TIMESTAMP": timestamp,
                "BWAAS-API-SIGNATURE": hexlify(signature),
                "Content-Type": "application/json"
            }

            try:
                res = requests.post(url=settings.DOMAIN+"/api/v1/notify/deposit", data=json.dumps(data),  headers=headers)
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
            print('Deposit Notify Error: ', e)
            return JsonResponse({
                'success': False,
                'message': serializer.errors,
                'result': []
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], serializer_class=CountUnusedAddressSerializer, url_path='generate-pending-withdrawal-orders')
    def generate_pending_withdrawal_orders(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            timestamp = str(int(time.time() * 1000))
            path = "/api/v1/withdrawal/orders?chain=" + serializer.validated_data['chain']

            sign_msg = create_sign_msg("GET", path, timestamp, {})
            sign_msg = sign_msg.encode("utf-8")

            signing_key = ed25519.SigningKey(settings.PRIVATE_KEY.encode("utf-8"), encoding="hex")
            signature = signing_key.sign(sign_msg)

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
            print('Generate Pending Withdrawal Orders Error: ', e)
            return JsonResponse({
                'success': False,
                'message': serializer.errors,
                'result': []
            }, status=status.HTTP_400_BAD_REQUEST)
