from django.contrib import admin

from apps.payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "amount", "status")
    search_fields = ("order_id", "full_name", "authority")
