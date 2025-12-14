import requests

from utils.load_env import env


class BaseZarin:
    CREATE_PAYMENT_URL = "https://payment.zarinpal.com/pg/v4/payment/request.json"
    REDIRECT_PAYMENT_URL = "https://payment.zarinpal.com/pg/StartPay/{}"
    VERIFY_PAYMENT_URL = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
    MERCHANT = env.MERCHANT

class CreatePayment(BaseZarin):

    def create_payment(self, amount, description, phone, order_id):
        data = {
            "merchant_id": self.MERCHANT,
            "amount": str(amount),
            "callback_url": env.BASE_SITE_ADDRESS + env.VERIFY_CALLBACK_ROUTE,
            "currency": "IRT",
            "description": description,
            "metadata": {
                "mobile": str(phone),
                "order_id": order_id,
                # "email": "info.test@example.com"
            }
        }
        response = requests.post(self.CREATE_PAYMENT_URL, json=data, timeout=20)

        if response.status_code == 200:
            js = response.json()
            if js['data']['code'] == 100:
                return js
        return False

class VerifyPayment(BaseZarin):

    def verify_payment(self, amount, authority):
        data = {
            "merchant_id": self.MERCHANT,
            "amount": str(amount),
            "authority": authority
        }
        response = requests.post(self.VERIFY_PAYMENT_URL, json=data, timeout=20)
        if response.status_code == 200:
            js = response.json()
            return js
        return False
