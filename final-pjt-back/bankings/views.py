from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from finance_recommendation.settings import BANKINGS_KEY
import requests

class DepositProductsViewSet(ModelViewSet):
    queryset = DepositProducts.objects.all()
    serializer_class = DepositProductsSerializer


class DepositOptionsViewSet(ModelViewSet):
    queryset = DepositOptions.objects.all()
    serializer_class = DepositOptionsSerializer


@api_view(['GET'])
def save_deposit_products(request):
    total_saved_base = 0  # 저장된 baseList 데이터 개수
    total_saved_option = 0  # 저장된 optionList 데이터 개수

    # API URL 구성
    ## 금융회사개요
    # url = f'https://finlife.fss.or.kr/finlifeapi/companySearch.json?auth={BANKINGS_KEY}&topFinGrpNo=020000&pageNo=1'

    ## 정기예금상품
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={BANKINGS_KEY}&topFinGrpNo=020000&pageNo=1'

    # ## 정기예금상품
    # url = f'https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={BANKINGS_KEY}&topFinGrpNo=020000&pageNo=1'

    resp = requests.get(url).json()

    baselist = resp.get("result").get("baseList")
    optionlist = resp.get("result").get("optionList")
    for base in baselist:
        save_data = {
            'dcls_month': base.get('dcls_month'), # '202001
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'etc_note': base.get('etc_note'),
            'join_deny': int(base.get('join_deny')),
            'join_member': base.get('join_member'),
            'join_way': base.get('join_way'),
            'spcl_cnd': base.get('spcl_cnd'),
        }
        for elem in save_data:
            if not save_data[elem]:
                save_data[elem] = -1
        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()
    for option in optionlist:
        save_data = {
            'dcls_month': option.get('dcls_month'), # '202001
            'fin_prdt_cd': option.get('fin_prdt_cd'),
            'intr_rate_type_nm': option.get('intr_rate_type_nm'),
            'intr_rate': option.get('intr_rate'),
            'intr_rate2': option.get('intr_rate2'),
            'save_trm': int(option.get('save_trm')),   
        }
        for elem in save_data:
            if not save_data[elem]:
                save_data[elem] = -1
        serializer = DepositOptionsSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save(product=DepositProducts.objects.get(fin_prdt_cd=save_data.get('fin_prdt_cd')))
    return Response({"message": "okay "})


@api_view(["GET", "POST"])
def deposit_products(request):
    if request.method == "GET":
        deposit_products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(deposit_products, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            # 중복 여부 확인
            if not DepositProducts.objects.filter(fin_prdt_cd=request.data.get("fin_prdt_cd")).exists():
                serializer.save()
                return Response(serializer.data)
            return Response({"message": "이미 존재하는 데이터입니다."}, status=400)
        return Response({"message": "잘못된 데이터입니다."}, status=400)


@api_view(["GET"])
def deposit_product_options(request, fin_prdt_cd):
    deposit_product = DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
    if not deposit_product:
        return Response({"message": "해당 상품이 존재하지 않습니다."}, status=404)

    depositoptions = DepositOptions.objects.filter(product=deposit_product)
    serializer = DepositOptionsSerializer(depositoptions, many=True)
    return Response(serializer.data)
