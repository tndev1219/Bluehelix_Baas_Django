import time
import requests
import ed25519
from binascii import hexlify, unhexlify
from django.http import JsonResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from apps.core.serializers import CountUnusedAddressSerializer
from apps.core.utils import create_sign_msg


class BaasViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'], serializer_class=CountUnusedAddressSerializer, url_path='count-unused-address')
    def CountUnusedAddress(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            timestamp = str(int(time.time() * 1000))
            path = "/api/v1/address/unused/count?chain="+settings.CHAIN

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
                print('-------------------------')
                print(res)
                print('-------------------------')
                print(res.text)
                print('-------------------------')
                return JsonResponse({
                'success': True,
                'message': 'Success',
                'result': res
            }, status=status.HTTP_200_OK)
            except ValueError:
                print('-- get_address_count error --', ValueError)
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

    # @action(detail=False, methods=['POST'], serializer_class=ResetPasswordSerializer, url_path='reset-password/(?P<reset_password_key>[a-zA-Z0-9]+)')
    # def reset_password(self, request, *args, **kwargs):
    #     try:
    #         context = {
    #             'request': request,
    #             'reset_password_key': kwargs['reset_password_key'],
    #         }
    #         serializer = self.serializer_class(data=request.data, context=context)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.reset(serializer.data)
    #         return JsonResponse(
    #             {
    #                 'success': True,
    #                 'message': 'Success',
    #                 'result': serializer.data,
    #             }, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         print('Reset password Error: ', e)
    #         return JsonResponse({
    #             'success': False,
    #             'message': serializer.errors,
    #             'result': []
    #         }, status=status.HTTP_400_BAD_REQUEST)

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
