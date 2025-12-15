import pytest
from django.test import Client
from django.urls import reverse
from pytest_mock import MockerFixture

from apps.payment.models import Payment
from utils.load_env import env


@pytest.mark.django_db
def test_payment_view_get(client: Client):
    minimum_payment = int(getattr(env, "MiNIMUM_PAYMENT", 10000))
    url = reverse("payment:payment-create")
    response = client.get(url)
    assert "minimum_payment" in response.context  # noqa: S101
    assert response.context["minimum_payment"] == minimum_payment # noqa: S101
    assert "payment/payment.html" in [t.name for t in response.templates] # noqa: S101

@pytest.mark.django_db
def test_payment_view_post_creates_payment(mocker: MockerFixture, client: Client):
    mocker.patch(
        "apps.payment.zarin.CreatePayment.create_payment",
        return_value={"data": {"code": 100, "authority": "AUTH123"}}
    )
    url = reverse("payment:payment-create")
    data = {"full_name": "John Doe", "phone": "09120000000", "amount": 20000, "description": "Test payment" }
    response = client.post(url, data)
    payment = Payment.objects.get(authority="AUTH123")
    assert payment.full_name == "John Doe" # noqa: S101
    assert response.status_code == 302 # noqa: S101
    assert "AUTH123" in response.url # noqa: S101

@pytest.mark.django_db
def test_verify_payment_success(mocker: MockerFixture, client: Client):
    payment = Payment.objects.create(
        full_name="John Doe",
        phone="09120000000",
        amount=20000,
        description="Test payment",
        order_id="ORDER123",
        authority="AUTH123",
        status=Payment.PaymentStatus.PENDING
    )
    mocker.patch(
        "apps.payment.zarin.VerifyPayment.verify_payment",
        return_value={"data": {"code": 100}}
    )
    mocker.patch(
        "apps.payment.models.send_payment_to_telegram",
        return_value={"ok": True}
    )

    url = reverse("payment:payment-verify")
    response = client.get(url, data={"Authority": "AUTH123", "Status": "OK"})
    payment.refresh_from_db()
    assert payment.status == Payment.PaymentStatus.SUCCESS # noqa: S101
    assert response.status_code == 200 # noqa: S101
    assert "payment/success.html" in [t.name for t in response.templates] # noqa: S101

@pytest.mark.django_db
def test_verify_payment_failed_status_nok(mocker: MockerFixture, client: Client):
    payment = Payment.objects.create(
        full_name="John Doe",
        phone="09120000000",
        amount=20000,
        description="Test payment",
        order_id="ORDER123",
        authority="AUTH123",
        status=Payment.PaymentStatus.PENDING
    )
    url = reverse("payment:payment-verify")
    response = client.get(url, {"Authority": "AUTH123", "Status": "NOK"})
    payment.refresh_from_db()

    assert payment.status == Payment.PaymentStatus.FAILED # noqa: S101
    assert response.status_code == 200 # noqa: S101
    assert "payment/failed.html" in [t.name for t in response.templates] # noqa: S101
