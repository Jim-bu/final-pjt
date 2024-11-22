from django.urls import path
from . import views


urlpatterns = [
    path('deposit-fetch-data/', views.deposit_fetch_data, name='deposit_fetch_data'),  # 예금 정보 저장
    path('deposit-get-products/', views.deposit_get_products, name='deposit_get_products'),  # 예금 정보 조회

    path('saving-fetch-data/', views.saving_fetch_data, name='saving_fetch_data'),  # 적금 정보 저장
    path('saving-get-products/', views.saving_get_products, name='saving_get_products'),  # 적금 정보 조회
]
