
import csv
import calendar

from decimal import Decimal, InvalidOperation
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction as db_transaction
from django.db.models import Sum, Q, Count
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse

from customers.models import Customer
from accounts.models import Account
from transactions.models import Transaction


# ==============================
# DASHBOARD
# ==============================

@login_required
def dashboard(request):
    total_customers = Customer.objects.count()
    total_accounts = Account.objects.count()

    total_balance = Account.objects.aggregate(
        total=Sum('balance')
    )['total'] or 0

    total_transactions = Transaction.objects.count()

    recent_transactions = (
        Transaction.objects
        .select_related('account', 'account__customer')
        .order_by('-transaction_date')[:5]
    )

    transaction_totals = (
        Transaction.objects
        .values('transaction_type')
        .annotate(total=Sum('amount'))
    )

    transaction_total_map = {
        item['transaction_type']: float(item['total'] or 0)
        for item in transaction_totals
    }

    deposit_total = transaction_total_map.get('DEPOSIT', 0)
    withdrawal_total = transaction_total_map.get('WITHDRAWAL', 0)

    account_type_totals = (
        Account.objects
        .values('account_type')
        .annotate(total=Count('account_id'))
    )

    account_type_map = {
        item['account_type']: item['total']
        for item in account_type_totals
    }

    account_type_labels = []
    account_type_counts = []

    account_type_choices = (
        Account._meta.get_field('account_type').choices
    )

    for value, label in account_type_choices:
        account_type_labels.append(str(label))
        account_type_counts.append(
            account_type_map.get(value, 0)
        )

    today = timezone.localdate()

    months = []

    for offset in range(5, -1, -1):
        month_index = today.year * 12 + (today.month - 1) - offset
        year, month_zero = divmod(month_index, 12)
        months.append((year, month_zero + 1))

    first_month = months[0]
    start_date = date(first_month[0], first_month[1], 1)

    monthly_transaction_map = {
        (year, month): 0
        for year, month in months
    }

    transaction_dates = (
        Transaction.objects
        .filter(transaction_date__gte=start_date)
        .values_list('transaction_date', flat=True)
    )

    for transaction_date in transaction_dates:
        month_key = (
            transaction_date.year,
            transaction_date.month
        )

        if month_key in monthly_transaction_map:
            monthly_transaction_map[month_key] += 1

    monthly_labels = []
    monthly_counts = []

    for year, month in months:
        month_label = f"{calendar.month_abbr[month]} {year}"

        monthly_labels.append(month_label)
        monthly_counts.append(
            monthly_transaction_map.get((year, month), 0)
        )

    context = {
        'total_customers': total_customers,
        'total_accounts': total_accounts,
        'total_balance': total_balance,
        'total_transactions': total_transactions,
        'recent_transactions': recent_transactions,
        'deposit_total': deposit_total,
        'withdrawal_total': withdrawal_total,
        'account_type_labels': account_type_labels,
        'account_type_counts': account_type_counts,
        'monthly_labels': monthly_labels,
        'monthly_counts': monthly_counts,
    }

    return render(request, 'dashboard.html', context)


# ==============================
# CUSTOMER MANAGEMENT
# ==============================

@login_required
def customer_list(request):
    search_query = request.GET.get('search', '').strip()

    customers = Customer.objects.all()

    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    context = {
        'customers': customers,
        'search_query': search_query,
        'total_customers': Customer.objects.count(),
    }

    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_create(request):
    errors = {}
    form_data = {}

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'address': request.POST.get('address', '').strip(),
        }

        for field, value in form_data.items():
            if not value:
                errors[field] = 'This field is required.'

        if form_data['email'] and Customer.objects.filter(
            email__iexact=form_data['email']
        ).exists():
            errors['email'] = 'This email address is already registered.'

        if form_data['phone'] and Customer.objects.filter(
            phone=form_data['phone']
        ).exists():
            errors['phone'] = 'This phone number is already registered.'

        if not errors:
            Customer.objects.create(**form_data)
            return redirect('customer_list')

    context = {
        'errors': errors,
        'form_data': form_data,
    }

    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    errors = {}

    form_data = {
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address,
    }

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'address': request.POST.get('address', '').strip(),
        }

        for field, value in form_data.items():
            if not value:
                errors[field] = 'This field is required.'

        if Customer.objects.filter(
            email__iexact=form_data['email']
        ).exclude(pk=customer.pk).exists():
            errors['email'] = 'This email address is already registered.'

        if Customer.objects.filter(
            phone=form_data['phone']
        ).exclude(pk=customer.pk).exists():
            errors['phone'] = 'This phone number is already registered.'

        if not errors:
            for field, value in form_data.items():
                setattr(customer, field, value)

            customer.save()
            return redirect('customer_list')

    return render(request, 'customers/customer_form.html', {
        'customer': customer,
        'errors': errors,
        'form_data': form_data,
        'is_edit': True,
    })


@login_required
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'customers/customer_confirm_delete.html', {
        'customer': customer,
    })


# ==============================
# ACCOUNT MANAGEMENT
# ==============================

@login_required
def account_list(request):
    search_query = request.GET.get('search', '').strip()

    accounts = Account.objects.select_related('customer').all()

    if search_query:
        accounts = accounts.filter(
            Q(account_number__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query)
        )

    total_accounts = Account.objects.count()

    total_balance = Account.objects.aggregate(
        total=Sum('balance')
    )['total'] or Decimal('0.00')

    context = {
        'accounts': accounts,
        'search_query': search_query,
        'total_accounts': total_accounts,
        'total_balance': total_balance,
    }

    return render(request, 'accounts/account_list.html', context)


@login_required
def account_create(request):
    errors = {}

    form_data = {
        'customer': '',
        'account_number': '',
        'account_type': 'SAVINGS',
        'balance': '0.00',
    }

    customers = Customer.objects.all()

    if request.method == 'POST':
        form_data = {
            'customer': request.POST.get('customer', '').strip(),
            'account_number': request.POST.get('account_number', '').strip(),
            'account_type': request.POST.get('account_type', '').strip(),
            'balance': request.POST.get('balance', '0.00').strip(),
        }

        customer = (
            Customer.objects.filter(pk=form_data['customer']).first()
            if form_data['customer'].isdigit()
            else None
        )

        if not customer:
            errors['customer'] = 'Please select a valid customer.'

        if not form_data['account_number']:
            errors['account_number'] = 'Account number is required.'
        elif Account.objects.filter(
            account_number=form_data['account_number']
        ).exists():
            errors['account_number'] = 'This account number already exists.'

        valid_account_types = [
            choice[0] for choice in
            Account._meta.get_field('account_type').choices
        ]

        if form_data['account_type'] not in valid_account_types:
            errors['account_type'] = 'Please select a valid account type.'

        try:
            opening_balance = Decimal(form_data['balance'])

            if not opening_balance.is_finite() or opening_balance < 0:
                errors['balance'] = 'Balance cannot be negative.'

        except (InvalidOperation, ValueError):
            opening_balance = Decimal('0.00')
            errors['balance'] = 'Please enter a valid balance.'

        if not errors:
            Account.objects.create(
                customer=customer,
                account_number=form_data['account_number'],
                account_type=form_data['account_type'],
                balance=opening_balance,
            )

            return redirect('account_list')

    return render(request, 'accounts/account_form.html', {
        'customers': customers,
        'errors': errors,
        'form_data': form_data,
    })


@login_required
def account_edit(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    customers = Customer.objects.all()
    errors = {}

    form_data = {
        'customer': str(account.customer_id),
        'account_number': account.account_number,
        'account_type': account.account_type,
    }

    if request.method == 'POST':
        form_data = {
            'customer': request.POST.get('customer', '').strip(),
            'account_number': request.POST.get('account_number', '').strip(),
            'account_type': request.POST.get('account_type', '').strip(),
        }

        customer = (
            Customer.objects.filter(pk=form_data['customer']).first()
            if form_data['customer'].isdigit()
            else None
        )

        if not customer:
            errors['customer'] = 'Please select a valid customer.'

        if not form_data['account_number']:
            errors['account_number'] = 'Account number is required.'
        elif Account.objects.filter(
            account_number=form_data['account_number']
        ).exclude(pk=account.pk).exists():
            errors['account_number'] = 'This account number already exists.'

        valid_account_types = [
            choice[0] for choice in
            Account._meta.get_field('account_type').choices
        ]

        if form_data['account_type'] not in valid_account_types:
            errors['account_type'] = 'Please select a valid account type.'

        if not errors:
            account.customer = customer
            account.account_number = form_data['account_number']
            account.account_type = form_data['account_type']

            # Balance is deliberately not changed here.
            account.save()

            return redirect('account_list')

    return render(request, 'accounts/account_form.html', {
        'account': account,
        'customers': customers,
        'errors': errors,
        'form_data': form_data,
        'is_edit': True,
    })


@login_required
def account_delete(request, account_id):
    account = get_object_or_404(Account, pk=account_id)

    if request.method == 'POST':
        account.delete()
        return redirect('account_list')

    return render(request, 'accounts/account_confirm_delete.html', {
        'account': account,
    })


# ==============================
# TRANSACTION MANAGEMENT
# ==============================

@login_required
def transaction_list(request):
    search_query = request.GET.get('search', '').strip()

    transactions = Transaction.objects.select_related(
        'account',
        'account__customer'
    ).all()

    if search_query:
        transactions = transactions.filter(
            Q(account__account_number__icontains=search_query) |
            Q(account__customer__first_name__icontains=search_query) |
            Q(account__customer__last_name__icontains=search_query) |
            Q(transaction_type__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    context = {
        'transactions': transactions,
        'search_query': search_query,
        'total_transactions': Transaction.objects.count(),
    }

    return render(request, 'transactions/transaction_list.html', context)


# ==============================
# DEPOSIT AND WITHDRAWAL
# ==============================

@login_required
def transaction_create(request):
    errors = {}

    form_data = {
        'account': '',
        'transaction_type': 'DEPOSIT',
        'amount': '',
        'description': '',
    }

    accounts = Account.objects.select_related('customer').all()

    if request.method == 'POST':
        form_data = {
            'account': request.POST.get('account', '').strip(),
            'transaction_type': request.POST.get(
                'transaction_type', ''
            ).strip(),
            'amount': request.POST.get('amount', '').strip(),
            'description': request.POST.get('description', '').strip(),
        }

        if form_data['transaction_type'] not in ['DEPOSIT', 'WITHDRAWAL']:
            errors['transaction_type'] = 'Please select a valid transaction type.'

        try:
            amount = Decimal(form_data['amount'])

            if not amount.is_finite() or amount <= 0:
                errors['amount'] = 'Amount must be greater than zero.'

        except (InvalidOperation, ValueError):
            amount = Decimal('0.00')
            errors['amount'] = 'Please enter a valid amount.'

        if not form_data['account'].isdigit():
            errors['account'] = 'Please select a valid account.'

        if not errors:
            try:
                with db_transaction.atomic():
                    account = Account.objects.select_for_update().get(
                        pk=form_data['account']
                    )

                    if form_data['transaction_type'] == 'DEPOSIT':
                        account.balance += amount

                    elif form_data['transaction_type'] == 'WITHDRAWAL':
                        if account.balance < amount:
                            errors['amount'] = (
                                'Insufficient balance. '
                                f'Available balance: ₹{account.balance}'
                            )
                        else:
                            account.balance -= amount

                    if not errors:
                        account.save(update_fields=['balance'])

                        Transaction.objects.create(
                            account=account,
                            transaction_type=form_data['transaction_type'],
                            amount=amount,
                            description=form_data['description'],
                        )

                if not errors:
                    return redirect('transaction_list')

            except Account.DoesNotExist:
                errors['account'] = 'The selected account does not exist.'

    return render(request, 'transactions/transaction_form.html', {
        'accounts': accounts,
        'errors': errors,
        'form_data': form_data,
    })


# ==============================
# TRANSACTION DELETE
# ==============================

@login_required
def transaction_delete(request, transaction_id):
    transaction_record = get_object_or_404(
        Transaction.objects.select_related('account'),
        pk=transaction_id
    )

    error = None

    if request.method == 'POST':
        try:
            with db_transaction.atomic():
                account = Account.objects.select_for_update().get(
                    pk=transaction_record.account_id
                )

                if transaction_record.transaction_type == 'DEPOSIT':
                    if account.balance < transaction_record.amount:
                        error = (
                            'This transaction cannot be deleted because '
                            'reversing it would make the account balance negative.'
                        )
                    else:
                        account.balance -= transaction_record.amount

                elif transaction_record.transaction_type == 'WITHDRAWAL':
                    account.balance += transaction_record.amount

                else:
                    error = (
                        'This transaction type cannot be safely reversed '
                        'automatically.'
                    )

                if not error:
                    account.save(update_fields=['balance'])
                    transaction_record.delete()

            if not error:
                return redirect('transaction_list')

        except Account.DoesNotExist:
            error = 'The related account no longer exists.'

    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction_record,
        'error': error,
    })


# ==============================
# REPORTS
# ==============================

@login_required
def reports(request):
    today = timezone.localdate()

    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()
    selected_type = request.GET.get('transaction_type', '').strip()

    errors = {}

    transactions = Transaction.objects.select_related(
        'account',
        'account__customer'
    ).all()

    # Validate and apply start date.
    if start_date:
        try:
            parsed_start_date = date.fromisoformat(start_date)
            transactions = transactions.filter(
                transaction_date__date__gte=parsed_start_date
            )
        except ValueError:
            errors['start_date'] = 'Please enter a valid start date.'

    # Validate and apply end date.
    if end_date:
        try:
            parsed_end_date = date.fromisoformat(end_date)
            transactions = transactions.filter(
                transaction_date__date__lte=parsed_end_date
            )
        except ValueError:
            errors['end_date'] = 'Please enter a valid end date.'

    # Check date range.
    if start_date and end_date and not errors:
        if parsed_start_date > parsed_end_date:
            errors['date_range'] = 'Start date cannot be after end date.'

    # Apply transaction type filter.
    valid_types = ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']

    if selected_type:
        if selected_type in valid_types:
            transactions = transactions.filter(
                transaction_type=selected_type
            )
        else:
            errors['transaction_type'] = 'Invalid transaction type.'

    if errors.get('date_range'):
        transactions = Transaction.objects.none()

    # Calculate summary values from filtered transactions.
    summary = transactions.aggregate(
        total_amount=Sum('amount'),
        deposit_total=Sum(
            'amount',
            filter=Q(transaction_type='DEPOSIT')
        ),
        withdrawal_total=Sum(
            'amount',
            filter=Q(transaction_type='WITHDRAWAL')
        ),
        transfer_total=Sum(
            'amount',
            filter=Q(transaction_type='TRANSFER')
        ),
    )

    total_amount = summary['total_amount'] or Decimal('0.00')
    deposit_total = summary['deposit_total'] or Decimal('0.00')
    withdrawal_total = summary['withdrawal_total'] or Decimal('0.00')
    transfer_total = summary['transfer_total'] or Decimal('0.00')

    total_transactions = transactions.count()

    # CSV export of the filtered transactions.
    if request.GET.get('export') == 'csv' and not errors:
        response = HttpResponse(
            content_type='text/csv'
        )

        response['Content-Disposition'] = (
            'attachment; filename="bankpro_transaction_report.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            'Transaction ID',
            'Account Number',
            'Customer Name',
            'Transaction Type',
            'Amount',
            'Date',
            'Description',
        ])

        for item in transactions.order_by('-transaction_date'):
            customer = item.account.customer

            writer.writerow([
                item.transaction_id,
                item.account.account_number,
                f'{customer.first_name} {customer.last_name}',
                item.get_transaction_type_display(),
                item.amount,
                timezone.localtime(
                    item.transaction_date
                ).strftime('%d-%m-%Y %I:%M %p'),
                item.description or '',
            ])

        return response

    context = {
        'transactions': transactions.order_by('-transaction_date'),
        'total_transactions': total_transactions,
        'total_amount': total_amount,
        'deposit_total': deposit_total,
        'withdrawal_total': withdrawal_total,
        'transfer_total': transfer_total,
        'start_date': start_date,
        'end_date': end_date,
        'selected_type': selected_type,
        'errors': errors,
    }

    return render(request, 'reports.html', context)
