from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from sklearn.metrics.pairwise import cosine_similarity
from .models import UserSurvey
from accounts.serializers import UserSerializer
from bankings.models import DepositBaseList, SavingBaseList
from bankings.serializers import DepositBaseListSerializer, SavingBaseListSerializer
import numpy as np
import logging


logger = logging.getLogger(__name__)

def convert_survey_to_vector(survey):
    try:
        vector = []
        # 매핑 테이블
        age_mapping = {'20대': 0, '30대': 1, '40대': 2, '50대': 3, '60대 이상': 4}
        risk_mapping = {'위험을 회피': 0, '중간': 1, '높은 위험 감수 가능': 2}
        period_mapping = {'6개월 이하': 0, '6개월 ~ 1년': 1, '1년 ~ 3년': 2, '3년 이상': 3}
        return_mapping = {'1% 이하': 0, '1% ~ 3%': 1, '3% ~ 5%': 2, '5% 이상': 3}

        # 각 항목을 매핑하며 기본값 적용
        vector.append(age_mapping.get(survey.age_group, 2))  # 기본값: 중간값
        vector.append(risk_mapping.get(survey.risk_tolerance, 1))
        vector.append(period_mapping.get(survey.investment_period, 1))
        vector.append(return_mapping.get(survey.expected_return, 1))

        # 벡터 출력 확인 (디버깅용)
        logger.debug(f"User vector: {vector}")
        return vector
    except Exception as e:
        raise ValueError(f"Error in convert_survey_to_vector: {e}")


def convert_product_to_vector(product, product_type='deposit'):
    try:
        vector = []

        # 기본값 설정
        max_rate = 0
        min_period = 36  # 기본값: 3년

        if product_type == 'deposit':
            # 예금 상품 옵션 데이터가 존재할 경우 처리
            if product.deposit_options.exists():
                max_rate = max([opt.intr_rate2 or 0 for opt in product.deposit_options.all()])
                min_period = min([int(opt.save_trm) for opt in product.deposit_options.all()])
        elif product_type == 'saving':
            # 적금 상품 옵션 데이터가 존재할 경우 처리
            if product.saving_options.exists():
                max_rate = max([opt.intr_rate2 or 0 for opt in product.saving_options.all()])
                min_period = min([int(opt.save_trm) for opt in product.saving_options.all()])

        # 기간을 기준으로 벡터 값 설정
        if min_period <= 6:
            vector.append(0)
        elif min_period <= 12:
            vector.append(1)
        elif min_period <= 36:
            vector.append(2)
        else:
            vector.append(3)

        # 금리를 기준으로 벡터 값 설정
        if max_rate <= 1:
            vector.append(0)
        elif max_rate <= 3:
            vector.append(1)
        elif max_rate <= 5:
            vector.append(2)
        else:
            vector.append(3)

        # 벡터 길이 고정 (항상 4)
        while len(vector) < 4:
            vector.append(0)  # 부족한 값은 기본값(0)으로 채움

        logger.debug(f"Product vector ({product_type}): {vector}")
        return vector
    except Exception as e:
        raise ValueError(f"Error in convert_product_to_vector: {e}")


def calculate_similarity(user_vector, product_vector):
    # 벡터 길이 확인
    if len(user_vector) != len(product_vector):
        logger.error(f"Dimension mismatch: user_vector({len(user_vector)}) vs product_vector({len(product_vector)})")
        raise ValueError(f"Dimension mismatch: user_vector({len(user_vector)}) vs product_vector({len(product_vector)})")

    # 유사도 계산
    return cosine_similarity([user_vector], [product_vector])[0][0]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_survey(request):
    try:
        # 요청 데이터 로깅
        logger.info(f"Received survey data: {request.data}")

        # 사용자 데이터 가져오기 및 보강
        user = request.user
        user_data = {
            'name': user.name or "Unknown",
            'age': user.age or 0,
            'money': user.money or 0.0,
            'salary': user.salary or 0.0,
        }

        # 데이터 유효성 검증 및 저장
        survey_data = request.data.copy()
        survey_data.update(user_data)  # 사용자 데이터를 설문 데이터와 병합

        serializer = UserSerializer(user, data=survey_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 설문 데이터 저장 로직
        survey = UserSurvey.objects.create(user=user, **request.data)
        return Response({"message": "Survey submitted successfully."}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in submit_survey: {e}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    try:
        latest_survey = UserSurvey.objects.filter(user=request.user).latest('created_at')
        user_vector = convert_survey_to_vector(latest_survey)
        logger.debug(f"User vector: {user_vector}")

        # 예금 상품 추천
        deposit_products = DepositBaseList.objects.prefetch_related('deposit_options').all()
        deposit_similarities = []
        for product in deposit_products:
            product_vector = convert_product_to_vector(product, 'deposit')
            logger.debug(f"Deposit product vector: {product_vector}")
            similarity = calculate_similarity(user_vector, product_vector)
            deposit_similarities.append((product, similarity))

        # 적금 상품 추천
        saving_products = SavingBaseList.objects.prefetch_related('saving_options').all()
        saving_similarities = []
        for product in saving_products:
            product_vector = convert_product_to_vector(product, 'saving')
            logger.debug(f"Saving product vector: {product_vector}")
            similarity = calculate_similarity(user_vector, product_vector)
            saving_similarities.append((product, similarity))

        # 유사도가 높은 순으로 정렬 후 상위 5개 상품 선택
        deposit_recommendations = sorted(deposit_similarities, key=lambda x: x[1], reverse=True)[:5]
        saving_recommendations = sorted(saving_similarities, key=lambda x: x[1], reverse=True)[:5]

        # 직렬화된 데이터 반환
        deposit_serializer = DepositBaseListSerializer([prod for prod, _ in deposit_recommendations], many=True)
        saving_serializer = SavingBaseListSerializer([prod for prod, _ in saving_recommendations], many=True)

        return Response({
            'deposit_recommendations': deposit_serializer.data,
            'saving_recommendations': saving_serializer.data
        }, status=status.HTTP_200_OK)

    except UserSurvey.DoesNotExist:
        logger.error("No survey found for the user.")
        return Response({'error': '설문 결과가 없습니다. 먼저 설문에 참여해주세요.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
