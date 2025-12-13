from django.db import models


class Payment(models.Model):
    class PaymentStatus(models.Choices):
        PENDING = "pending"
        SUCCESS = "success"
        FAILED = "failed"

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
