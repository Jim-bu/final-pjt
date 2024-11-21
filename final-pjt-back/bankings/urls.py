from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositProductsViewSet, DepositOptionsViewSet, save_deposit_products, deposit_products, deposit_product_options


# Router 생성
router = DefaultRouter()
router.register(r'deposit-products', DepositProductsViewSet)
router.register(r'deposit-options', DepositOptionsViewSet)

urlpatterns = [
    path('', include(router.urls)),  # /api/ 경로 아래에 모든 Router URL 포함
    # 정기예금 상품 목록 DB에 저장
    path('save-deposit-products/', save_deposit_products),
    # 전체 정기예금 상품 목록 출력 & 데이터 삽입
    path('deposit-products/', deposit_products),
    # 특정 상품의 옵션 리스트 출력
    path('deposit-product-options/<str:fin_prdt_cd>/', deposit_product_options),
    # 가입 기간에 상관없이 최고 금리가 가장 높은 금융 상품과 해당 상품의 옵션 리스트 출력
]
