from django.urls import path
from . import views

urlpatterns = [
    path('user_all/', views.user_all, name='user_all'),
    path('user_info/', views.user_info, name='user_info'),  # 현재 사용자 정보 조회
    path('user_update/', views.user_update, name='user_update'),
]
