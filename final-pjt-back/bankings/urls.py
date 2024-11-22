from django.urls import path
from . import views


urlpatterns = [
    path('deposit-fetch-data/', views.deposit_fetch_data, name='deposit_fetch_data'),
    path('deposit-get-products/', views.deposit_get_products, name='deposit_get_products'),

    path('saving-fetch-data/', views.saving_fetch_data, name='saving_fetch_data'),
    path('saving-get-products/', views.saving_get_products, name='saving_get_products'),
]