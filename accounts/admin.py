
from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = (
        'account_id',
        'account_number',
        'customer',
        'account_type',
        'balance',
        'created_at'
    )

    search_fields = (
        'account_number',
        'customer__first_name',
        'customer__last_name',
    )

    list_filter = ('account_type', 'created_at')
