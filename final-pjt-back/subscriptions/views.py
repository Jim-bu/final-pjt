from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_405_METHOD_NOT_ALLOWED
from .models import SubscribedProduct
from .serializers import SubscribedProductSerializer

## 금융 상품 구독/취소 API
@api_view(['POST'])
def toggle_subscribed_product(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            product_id = data.get('product_id')
            product_name = data.get('product_name')

            if not product_id or not product_name:
                return Response({"error": "Product ID and name are required."}, status=HTTP_400_BAD_REQUEST)

            # 이미 구독된 상품인지 확인
            existing_subscription = SubscribedProduct.objects.filter(
                user=request.user,
                product_id=product_id
            ).first()

            if existing_subscription:
                # 이미 구독된 경우 -> DB에서 삭제
                existing_subscription.delete()
                return Response({"message": f"'{product_name}' 구독이 취소되었습니다."}, status=HTTP_200_OK)
            else:
                # 구독되지 않은 경우 -> DB에 추가
                subscribed_product = SubscribedProduct.objects.create(
                    user=request.user,
                    product_id=product_id,
                    product_name=product_name
                )

                serializer = SubscribedProductSerializer(subscribed_product)

                # 터미널에 이메일 내용 출력
                email_message = (
                    f"구독 완료: 금융 상품 알림\n"
                    f"안녕하세요, {request.user.name or request.user.username}님.\n\n"
                    f"'{product_name}' 금융 상품에 성공적으로 구독하셨습니다.\n"
                    f"자세한 내용은 프로필 페이지에서 확인하실 수 있습니다.\n\n"
                    f"감사합니다."
                )
                print(email_message)

                return Response(serializer.data, status=HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

    return Response({"error": "Invalid request method."}, status=HTTP_405_METHOD_NOT_ALLOWED)


## 사용자 구독 목록 조회 API
@api_view(['GET'])
def my_subscribed_products(request):
    if request.method == 'GET':
        subscribed_products = SubscribedProduct.objects.filter(user=request.user)
        serializer = SubscribedProductSerializer(subscribed_products, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    return Response({"error": "Invalid request method."}, status=HTTP_405_METHOD_NOT_ALLOWED)
