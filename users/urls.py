from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views, adminviews

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    
    path('logout/', views.log_out, name='logout'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    # Updated password reset URLs with correct names
    path('password_reset/', auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             success_url='done/'
         ), 
         name='password_reset'),
    
    # path('password_reset/done/', 
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='registration/password_reset_done.html'
    #      ), 
    #      name='password_reset_done'),

    path('password_reset/done/',  # NOT 'password_reset/done/'
            auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'  # NOT password_reset_done.html
        ), 
     name='password_reset_done'),
    
    # path('reset/<uidb64>/<token>/', 
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='registration/password_reset_confirm.html',
    #          success_url='/users/reset/done/'
    #      ), 
    #      name='password_reset_confirm'),

    path('reset/<uidb64>/<token>/', 
     auth_views.PasswordResetConfirmView.as_view(
         template_name='registration/password_reset_confirm.html',
         success_url=reverse_lazy('users:password_reset_complete')  # Changed from '/users/reset/done/'
     ), 
     name='password_reset_confirm'),

    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),



    #Customer Panel
    path('customer/dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('customer/profile/', views.customer_profile, name='customer-profile'),
    path('customer/orders/', views.orders, name='customer-orders'),
    path('customer/orders/<str:type>/<int:id>', views.order_details, name='customer-order-details'),
    path('customer/orders-records/', views.order_records, name='customer-orders-records'),

    path('customer/quote-orders/', views.quotes, name='customer-quotes'),
    path('customer/quote-records/', views.quote_records, name='customer-quote-records'),
    path('digitizing-quote/<int:pk>/', views.digitizing_quote_details, name='digitizing-quote-detail'),
    path('patch-quote/<int:pk>/', views.patch_quote_details, name='patch-quote-detail'),
    path('vector-quote/<int:pk>/', views.vector_quote_details, name='vector-quote-detail'),

    path('accept-quote/<str:quote_type>/<int:pk>/', views.accept_quote, name='accept-quote'),




    #Admin Panel
    path('admin/dashboard/', adminviews.admin_dashboard, name='admin-dashboard'),
    path('admin/all-receivables/', adminviews.admin_all_receivables, name='admin-all-receivables'),
    path('admin/find-invoice/', adminviews.admin_invoice_list, name='admin-invoice-list'),
    path('admin/inprocesss-orders/', adminviews.inprocess_orders, name='admin-inprocess-orders'),
    path('admin/order-details/<int:pk>/<str:order_type>/', adminviews.admin_order_details, name='admin-order-details'),
]
