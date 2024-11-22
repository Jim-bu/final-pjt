from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_all(request):
    users = User.objects.all()    # 모든 유저 가져오기
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_info(request):
    user = request.user    # 현재 로그인된 사용자
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_update(request):
    user = request.user    # 현재 로그인된 사용자

    # 요청 데이터로 사용자 업데이트
    serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True는 선택적 업데이트를 허용
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User fields updated successfully.",
            "updated_data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
