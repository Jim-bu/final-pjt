from django.urls import path
from . import views

urlpatterns = [
    path('news-fetch-data/', views.news_fetch_data, name='news_fetch_data'),
    path('news-get-data/', views.news_get_data, name='news_get_data'),
]
