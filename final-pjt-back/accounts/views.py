from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()  # 모든 User 데이터를 가져옴
    serializer_class = UserSerializer

@api_view(['GET'])
def get_all_user_fields(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_current_user(request):
    # 인증된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return Response({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)

    # 현재 사용자 직렬화
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def update(request, user_id):
    try:
        user = User.objects.get(id=user_id)  # 사용자 ID로 특정 사용자 조회
    except User.DoesNotExist:
        return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    # Partial 업데이트 (일부 필드만 업데이트)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

