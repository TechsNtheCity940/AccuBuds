from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_pin(request):
    """
    Employee PIN login.

    POST { "pin": "1234", "terminal": "420" }

    Returns { token, user_id, username, terminal } or 401.
    """
    pin = request.data.get('pin', '').strip()
    terminal = request.data.get('terminal', '').strip()

    if not pin or len(pin) != 4 or not pin.isdigit():
        return Response(
            {'detail': 'PIN must be exactly 4 digits'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = CustomUser.objects.get(login_pin=pin, is_active=True)
    except CustomUser.DoesNotExist:
        return Response(
            {'detail': 'Invalid PIN'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'terminal': terminal,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    """Invalidate the current token."""
    token_key = request.data.get('token', '')
    Token.objects.filter(key=token_key).delete()
    return Response({'status': 'ok'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
