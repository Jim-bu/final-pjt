from rest_framework.decorators import api_view
from rest_framework.response import Response
from finance_recommendation.settings import CURRENCIES_KEY
from .models import Exchange
from .serializers import ExchangeSerializer
import requests

API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={CURRENCIES_KEY}&data=AP01'

@api_view(['GET'])
def exchange_fetch_data(request):
    response = requests.get(API_URL)

    data = response.json()

    for item in data:
        defaults = {
            'ttb': item.get('ttb', ''),  # 전신환(송금) 받으실 때
            'tts': item.get('tts', ''),  # 전신환(송금) 보내실 때
            'deal_bas_r': item.get('deal_bas_r', ''),  # 매매기준율
            'bkpr': item.get('bkpr', ''),  # 장부가격
            'yy_efee_r': item.get('yy_efee_r', ''),  # 연이율 수수료율
            'ten_dd_efee_r': item.get('ten_dd_efee_r', ''),  # 10일 수수료율
            'kftc_bkpr': item.get('kftc_bkpr', ''),  # KFTC 장부가격
            'kftc_deal_bas_r': item.get('kftc_deal_bas_r', ''),  # KFTC 매매기준율
            'cur_nm': item.get('cur_nm', ''),  # 통화명
        }

        Exchange.objects.update_or_create(
            cur_unit=item.get('cur_unit', ''),  # 통화 단위로 고유값 결정
            defaults=defaults
        )

    return Response({"message": "Exchange rates fetched and stored successfully."})

@api_view(['GET'])
def exchange_get_data(request):
    exchanges = Exchange.objects.all()
    serializer = ExchangeSerializer(exchanges, many=True)
    return Response(serializer.data)