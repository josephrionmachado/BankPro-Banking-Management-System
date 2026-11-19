
from django.db import models
from accounts.models import Account


class Transaction(models.Model):

    transaction_id = models.AutoField(primary_key=True)

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('DEPOSIT', 'Deposit'),
            ('WITHDRAWAL', 'Withdrawal'),
            ('TRANSFER', 'Transfer'),
        ]
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(blank=True, null=True)

    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

    class Meta:
        db_table = 'transactions'
        ordering = ['-transaction_date']
