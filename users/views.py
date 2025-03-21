from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from users.models import User
from users.serializers import UserSerializer, UserRegistrationSerializer
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    {'message': 'User registered successfully', 'user': serializer.data},
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )
            except IntegrityError as e:
                error_message = str(e)
                if 'email' in error_message.lower():
                    return Response(
                        {'error': 'A user with this email already exists.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif 'username' in error_message.lower():
                    return Response(
                        {'error': 'A user with this username already exists.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {'error': 'Failed to register user due to a constraint violation.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='me')
    def me(self, request):
        """
        Get the current authenticated user's profile
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)