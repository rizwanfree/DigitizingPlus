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
    path('customer/orders/<str:type>/<int:id>/edit/', views.edit_order, name='edit-order'),


    path('customer/quote-orders/', views.quotes, name='customer-quotes'),
    path('customer/quote-records/', views.quote_records, name='customer-quote-records'),
    path('digitizing-quote/<int:pk>/', views.digitizing_quote_details, name='digitizing-quote-detail'),
    path('patch-quote/<int:pk>/', views.patch_quote_details, name='patch-quote-detail'),
    path('vector-quote/<int:pk>/', views.vector_quote_details, name='vector-quote-detail'),

    path('quotes/digitizing/edit/<int:id>/', views.edit_digitizing_quote, name='edit-digitizing-quote'),
    path('quotes/patch/edit/<int:id>/', views.edit_patch_quote, name='edit-patch-quote'),
    path('quotes/vector/edit/<int:id>/', views.edit_vector_quote, name='edit-vector-quote'),

    path('accept-quote/<str:quote_type>/<int:pk>/', views.accept_quote, name='accept-quote'),


    path('invoices/', views.invoice_list, name='invoice-list'),
    path('invoices/<int:invoice_id>/', views.invoice_detail, name='invoice-detail'),





    #Admin Panel

    path('admin/impersonate/<int:user_id>/', adminviews.start_impersonate, name='start-impersonate'),
    path('admin/stop-impersonate/', adminviews.stop_impersonate, name='stop-impersonate'),


    path('admin/dashboard/', adminviews.admin_dashboard, name='admin-dashboard'),
    path('admin/company-info/', adminviews.update_company_info, name='admin-company-info'),
    path('admin/all-receivables/', adminviews.admin_all_receivables, name='admin-all-receivables'),
    path('admin/user-list/', adminviews.user_list, name='admin-user-list'),
    path('admin/user-details/<int:pk>/', adminviews.user_detail, name='admin-user-detail'),
    path('admin/add-credit-card/<int:pk>/', adminviews.add_credit_card, name='admin-add-card'),


    path('admin/find-invoice/', adminviews.admin_invoice_list, name='admin-invoice-list'),
    path('admin/invoices/<int:invoice_id>/detail/', adminviews.invoice_detail, name='admin-invoice-detail'),

    #path('admin/inprocesss-orders/', adminviews.inprocess_orders, name='admin-inprocess-orders'),
    path('admin/inprocess-digitizing-orders/', adminviews.inprocess_digitizing_orders, name='admin-inprocess-digitizing-orders'),
    path('admin/inprocess-patch-orders/', adminviews.inprocess_patch_orders, name='admin-inprocess-patch-orders'),
    path('admin/inprocess-vector-orders/', adminviews.inprocess_vector_orders, name='admin-inprocess-vector-orders'),

    path('admin/all-digitizing-orders/', adminviews.all_digitizing_orders, name='admin-all-digitizing-orders'),
    path('admin/all-patch-orders/', adminviews.all_patch_orders, name='admin-all-patch-orders'),
    path('admin/all-vector-orders/', adminviews.all_vector_orders, name='admin-all-vector-orders'),


    path('admin/inprocess-digitizing-quotes/', adminviews.inprocess_digitizing_quotes, name='admin-inprocess-digitizing-quotes'),
    path('admin/inprocess-patch-quotes/', adminviews.inprocess_patch_quotes, name='admin-inprocess-patch-quotes'),
    path('admin/inprocess-vector-quotes/', adminviews.inprocess_vector_quotes, name='admin-inprocess-vector-quotes'),


    path('admin/digitizing-order-details/<int:pk>/', adminviews.finalize_digitizing_order, name='admin-digitizing-order-details'),
    path('admin/vector-order-details/<int:pk>/', adminviews.vector_orders_details, name='admin-vector-order-details'),
    path('orders/<int:pk>/update-admin-instructions/', adminviews.update_admin_instructions, name='update_admin_instructions'),



    path('admin/invoices/paid/', adminviews.paid_invoices, name='admin-paid-invoices'),
    path('admin/invoices/unpaid/', adminviews.unpaid_invoices, name='admin-unpaid-invoices'),

    
    path('admin/customer/<int:user_id>/unpaid-invoices/', adminviews.customer_unpaid_invoices, name='admin-customer-unpaid-invoices'),
    path('admin/invoice/<int:invoice_id>/pay/', adminviews.manual_payment, name='admin-manual-payment'),
    path('admin/invoice/<int:invoice_id>/pay/<int:payment_id>/', adminviews.manual_payment, name='admin-edit-payment'),


]
