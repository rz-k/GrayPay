from django.db import models
from django_lifecycle import AFTER_SAVE, LifecycleModel, hook
from django_lifecycle.conditions import WhenFieldValueIs, WhenFieldValueWas

from utils.utils import run_function_in_thread, send_payment_to_telegram


class Payment(LifecycleModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    full_name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    amount = models.PositiveBigIntegerField()
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    authority = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    response_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.full_name or f"Payment #{self.id}"

    @hook(
        AFTER_SAVE,
        condition=(
            WhenFieldValueWas("status", value="pending")
            & WhenFieldValueIs("status", value="success")
        )
    )
    def telegram_notify(self):
        run_function_in_thread(send_payment_to_telegram, self)
