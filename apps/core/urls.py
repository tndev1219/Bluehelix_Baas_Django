from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.BaasViewSet, basename='api')

urlpatterns = [
    # url(r'login/', views.Login.as_view(), name='login'),
    url(r'', include(router.urls)),
    # url(r'forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    # url(r'reset-password/(?P<reset_password_key>\w+)/$', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    # url(r'reset-email/', views.ResetEmail.as_view(), name='reset_email'),
    # url(r'change-password/', views.ChangePassword.as_view(), name='change_password'),
    # url(r'signup/', views.SignUpAPIView.as_view(), name='sign_up'),
    # url(r'create-checkout-session/', views.CreateCheckoutSessionAPIView.as_view(), name='create_checkout_session'),
    # url(r'reflect-subscription-info/', views.ReflectSubscriptionInfoAPIView.as_view(), name='reflect_subscription_info'),
    # url(r'cancel-subscription/', views.CancelSubscriptionAPIView.as_view(), name='cancel_subscription'),
    # url(r'save-new-card-info/', views.SaveNewCardInfoAPIView.as_view(), name='save_new_card_info'),
    # url(r'update-payment-method/', views.UpdatePaymentMethodAPIView.as_view(), name='update_payment_method')
]
