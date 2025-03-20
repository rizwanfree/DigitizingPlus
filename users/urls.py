from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    
    path('logout/', views.log_out, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    #Customer Panel
    path('customer/dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('customer/orders/', views.orders, name='customer-orders'),
    path('customer/orders/<str:type>/<int:id>', views.order_details, name='customer-order-details'),
    path('customer/orders-records/', views.order_records, name='customer-orders-records'),

    path('customer/quote-orders/', views.quotes, name='customer-quotes'),
    path('customer/quote-records/', views.quote_records, name='customer-quote-records'),




    #Admin Panel
    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
]
