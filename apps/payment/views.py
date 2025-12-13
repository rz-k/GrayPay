from django.db import transaction
from django.shortcuts import redirect, render
from django.views import View

from apps.payment.models import Payment
from apps.payment.zarin import CreatePayment, VerifyPayment
from utils.load_env import env
from utils.logger import deposit_error_logger, deposit_logger
from utils.utils import generate_payment_id


class PaymentView(View):
    template_name = "payment/payment.html"

    def get(self, request):
        minimum_payment = int(env.MiNIMUM_PAYMENT)
        context = {"minimum_payment": minimum_payment}
        return render(request, self.template_name, context)

    def post(self, request):
        full_name = request.POST.get("full_name", "") or None
        phone = request.POST.get("phone", "") or None
        amount = request.POST.get("amount", "") or 10000
        description = request.POST.get("description", "") or "user payment"
        order_id = generate_payment_id()
        create = CreatePayment()
        response_create_payment = create.create_payment(amount=amount, description=description, phone=phone, order_id=order_id)
        if not response_create_payment:
            return redirect("payment:payment-create")

        redirect_payment_url = create.REDIRECT_PAYMENT_URL.format(response_create_payment['data']['authority'])
        Payment.objects.create(
            full_name=full_name,
            phone=phone,
            amount=amount,
            description=description,
            order_id=order_id,
            authority=response_create_payment['data']['authority']
        )
        return redirect(redirect_payment_url)

class VerifyPaymentView(View):
    template_name = "payment/payment.html"
    template_failed = "payment/failed.html"
    template_success = "payment/success.html"

    def get(self, request):
        authority = request.GET.get("Authority")
        status = request.GET.get("Status")
        with transaction.atomic():
            try:
                payment = (
                    Payment.objects
                    .select_for_update()
                    .get(
                        authority=authority,
                        status=Payment.PaymentStatus.PENDING
                    )
                )
            except Payment.DoesNotExist:
                deposit_error_logger.warning(
                    "Payment not found or already processed | authority=%s",
                    authority
                )
                return redirect("payment:payment-create")

            except Exception as e:
                deposit_error_logger.exception(
                    f"Exception while verifying payment: {e} | authority=%s",
                    authority
                )
                context = {
                    "error": "خطایی رخ داده است",
                    "payment": payment
                }
                return render(request, self.template_failed, context)

            if status == "NOK":
                deposit_logger.info(
                    "Payment canceled by gateway | authority=%s",
                    authority
                )
                context = {
                    "error": "خطای نامشخص",
                    "payment": payment
                }
                return render(request, self.template_failed, context)


            verify = VerifyPayment()
            response_verify = verify.verify_payment(amount=payment.amount, authority=payment.authority)
            if not response_verify:
                deposit_error_logger.error(
                    "Empty verify response | authority=%s",
                    authority
                )
                context = {
                    "error": "خطای نامشخص",
                    "payment": payment
                }
                return render(request, self.template_failed, context)

            if response_verify['data']['code'] == 100:
                payment.status=Payment.PaymentStatus.SUCCESS
                payment.response_data=response_verify
                payment.save()
                deposit_logger.info(
                    "Payment verified successfully | authority=%s | amount=%s",
                    authority,
                    payment.amount
                )
                context = {"payment": payment}
                return render(request, self.template_success, context)

            deposit_error_logger.warning(
                "Payment verification failed | authority=%s | code=%s | response=%s",
                authority,
                response_verify['data']['code'],
                response_verify
            )
        return redirect("payment:payment-create")
