from django.contrib import admin
from django.urls import path, include
from .views import submit_survey

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submit-survey/', submit_survey, name='submit-survey'),
]
