import pytest

from apps.payment.models import Payment


@pytest.mark.django_db
def test_telegram_notify_hook_runs_only_on_status_change(mocker):

    mock_send = mocker.patch(
        "apps.payment.models.send_payment_to_telegram",
        return_value={"ok": True}
    )

    payment1 = Payment.objects.create(
        full_name="Alice",
        phone="09120000000",
        amount=10000,
        description="Test payment",
        order_id="ORDER001",
        authority="AUTH001",
        status=Payment.PaymentStatus.PENDING
    )

    payment1.status = Payment.PaymentStatus.SUCCESS
    payment1.save()
    mock_send.assert_called_once_with(payment1)

    payment2 = Payment.objects.create(
        full_name="Bob",
        phone="09120000001",
        amount=15000,
        description="Test payment 2",
        order_id="ORDER002",
        authority="AUTH002",
        status=Payment.PaymentStatus.SUCCESS
    )
    mock_send.reset_mock()
    payment2.save()
    mock_send.assert_not_called()
