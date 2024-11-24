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
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        updated_user = UserSerializer(user, context={'request': request}).data
        return Response({
            "message": "User fields updated successfully.",
            "updated_data": updated_user
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
