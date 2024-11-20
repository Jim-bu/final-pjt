from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .serializers import *
from .models import *
from finance_recommendation.settings import CURRENCIES_KEY


@api_view(['GET'])
def exchange(request):
    # API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={CURRENCIES_KEY}&data=AP01'
    API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={CURRENCIES_KEY}&searchdate=20220516&data=AP01'

    result = requests.get(API_URL).json()
    for item in result:
            Exchange.objects.update_or_create(
                cur_unit=item.get('cur_unit'),
                defaults={
                    'cur_nm': item.get('cur_nm'),
                    'ttb': item.get('ttb'),
                    'tts': item.get('tts'),
                    'deal_bas_r': item.get('deal_bas_r'),
                    'bkpr': item.get('bkpr'),
                    'yy_efee_r': item.get('yy_efee_r'),
                    'ten_dd_efee_r': item.get('ten_dd_efee_r'),
                    'kftc_deal_bas_r': item.get('kftc_deal_bas_r'),
                    'kftc_bkpr': item.get('kftc_bkpr'),
                }
        )
    return Response(result)
