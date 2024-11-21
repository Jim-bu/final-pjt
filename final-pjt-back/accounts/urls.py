from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, update, get_current_user, get_all_user_fields

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('update/<int:user_id>/', update, name='update'),
    path('user-fields/', get_all_user_fields, name='get_all_user_fields'),
    # path('user/', get_current_user, name='get_current_user'),  # 현재 사용자 정보
]