from django.urls import path

from . import views


app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('features/', views.features, name='features'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('pricing/', views.pricing, name='pricing'),
    path('payment/', views.payment, name='payment'),
    path('contact/', views.contact, name='contact'),
    path('vector-digitizing/', views.vector, name='vector'),
    path('patches/', views.patches, name='patches'),
]
