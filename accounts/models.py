
from django.db import models
from customers.models import Customer


class Account(models.Model):

    account_id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='accounts'
    )

    account_number = models.CharField(
        max_length=20,
        unique=True
    )

    account_type = models.CharField(
        max_length=20,
        choices=[
            ('SAVINGS', 'Savings'),
            ('CURRENT', 'Current'),
        ]
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_number

    class Meta:
        db_table = 'accounts'
        ordering = ['-created_at']
