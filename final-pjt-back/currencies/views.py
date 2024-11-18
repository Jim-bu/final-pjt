from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .serializers import *
from .models import *
from my_api.settings import CURRENCIES_KEY


@api_view(['GET'])
def exchange(request):
    # API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={CURRENCIES_KEY}&data=AP01'
    API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={CURRENCIES_KEY}&searchdate=20220516&data=AP01'

    result = requests.get(API_URL).json()

    return Response(result)
