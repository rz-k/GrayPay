from django.shortcuts import redirect, render
from django.views import View

from utils.load_env import env


class PaymentView(View):
    template_name = "payment/payment.html"

    def get(self, request):
        minimum_payment = int(env.MiNIMUM_PAYMENT)
        context = {"minimum_payment": minimum_payment}
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST.get("my_field")
        return redirect("same_view_name")
