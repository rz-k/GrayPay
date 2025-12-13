from django.shortcuts import redirect, render
from django.views import View

from apps.payment.models import Payment
from utils.load_env import env
from utils.utils import generate_payment_id
from apps.payment.zarin import CreatePayment


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
        #<QueryDict: {'csrfmiddlewaretoken': ['n2f78CqMPNZOzPksfOe1DDeMR4ExWbdwhMz9lqzjvFuyD6i4IqqrHPf1Vp0k3upt'], 'full_name': ['یرریتت'], 'phone': [''], 'amount': ['500000'], 'description': ['']}>
        # print(request.data)
        # data = request.POST.get("my_field")
        return redirect(redirect_payment_url)

