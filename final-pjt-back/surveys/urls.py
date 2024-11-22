from django.urls import path
from .views import submit_survey


urlpatterns = [
    path('submit-survey/', submit_survey, name='submit-survey'),
]
