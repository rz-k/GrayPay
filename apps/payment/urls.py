from django.urls import path

from apps.payment.views import PaymentView, VerifyPaymentView

app_name = "payment"

urlpatterns = [
    path('', PaymentView.as_view(), name='payment-create'),
    path('verify-transaction/', VerifyPaymentView.as_view(), name='payment-verify'),
]
