from django.contrib.auth import get_user_model
from rest_framework import permissions, serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    default_error_messages = {
        'invalid_credentials': 'Invalid email or password.',
        'inactive': 'User account is disabled.',
    }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed(self.error_messages['invalid_credentials']) from exc

        if not user.check_password(password):
            raise AuthenticationFailed(self.error_messages['invalid_credentials'])

        if not user.is_active:
            raise AuthenticationFailed(self.error_messages['inactive'])

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.get_full_name() or user.username,
                'is_staff': user.is_staff,
                'role': 'admin' if user.is_staff else 'external',
            },
        }


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
