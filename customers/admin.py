
from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'customer_id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'created_at'
    )

    search_fields = ('first_name', 'last_name', 'email', 'phone')

    list_filter = ('created_at',)
