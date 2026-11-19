
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    dashboard,
    customer_list,
    customer_create,
    customer_edit,
    customer_delete,
    account_list,
    account_create,
    account_edit,
    account_delete,
    transaction_list,
    transaction_create,
    transaction_delete,
    reports,
)


urlpatterns = [
    # Authentication
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Customers
    path('customers/', customer_list, name='customer_list'),
    path('customers/add/', customer_create, name='customer_create'),
    path('customers/edit/<int:customer_id>/', customer_edit, name='customer_edit'),
    path('customers/delete/<int:customer_id>/', customer_delete, name='customer_delete'),

    # Accounts
    path('accounts/', account_list, name='account_list'),
    path('accounts/add/', account_create, name='account_create'),
    path('accounts/edit/<int:account_id>/', account_edit, name='account_edit'),
    path('accounts/delete/<int:account_id>/', account_delete, name='account_delete'),

    # Transactions
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/add/', transaction_create, name='transaction_create'),
    path('transactions/delete/<int:transaction_id>/', transaction_delete, name='transaction_delete'),

    # Reports
    path('reports/', reports, name='reports'),

    # Django Admin
    path('admin/', admin.site.urls),
]
