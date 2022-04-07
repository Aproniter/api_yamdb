from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UsersSerializer
from api.permissions import *


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AdminOnly]
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    search_fields = ('^username',)


class UserApiView(APIView):
    serializer_class = UsersSerializer
    permission_classes = [AuthorPermission]

    def get(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if 'role' not in serializer.validated_data:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
