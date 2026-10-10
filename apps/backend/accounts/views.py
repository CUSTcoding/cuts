import binascii

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
)
from .models import Role, StatusUser

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class MeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.role != Role.CLIENTE:
            return Response(
                {"detail": "Esta conta não pode ser apagada por esta via."},
                status=status.HTTP_403_FORBIDDEN,
            )

        password = request.data.get("password")
        if not password or not user.check_password(password):
            return Response(
                {"password": "Confirma a palavra-passe para apagar a conta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Desativa em vez de apagar fisicamente para preservar históricos.
        user.is_active = False
        user.status = StatusUser.INATIVO
        user.save(update_fields=["is_active", "status", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ("PUT", "PATCH"):
            kwargs.setdefault("partial", self.request.method == "PATCH")
        return super().get_serializer(*args, **kwargs)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "O token refresh é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return Response(
                {"detail": "Token refresh inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return Response(
                {"new_password": list(exc.messages)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response({"detail": "Palavra-passe alterada com sucesso."})


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        if isinstance(email, str):
            user = User.objects.filter(email__iexact=email.strip()).first()
        else:
            user = None

        if user and user.is_active:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = getattr(
                settings,
                "FRONTEND_RESET_URL",
                "http://localhost:3000/reset-password/",
            )
            reset_url = f"{reset_url}?uid={uid}&token={token}"

            send_mail(
                subject="Recuperação da palavra-passe",
                message=(
                    "Recebeste este email porque foi solicitada "
                    "a recuperação da tua palavra-passe.\n\n"
                    f"Abre este link para continuar: {reset_url}\n\n"
                    "Se não fizeste este pedido, ignora este email."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

        return Response({
            "detail": (
                "Se o email estiver registado, receberás "
                "instruções para recuperar a palavra-passe."
            )
        })


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")
        password_confirm = request.data.get("password_confirm")

        if not all([uid, token, password, password_confirm]):
            return Response(
                {"detail": "Todos os campos são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != password_confirm:
            return Response(
                {"password_confirm": "As palavras-passe não coincidem."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (
            TypeError,
            ValueError,
            OverflowError,
            binascii.Error,
            User.DoesNotExist,
        ):
            return Response(
                {"detail": "Link de recuperação inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Link de recuperação inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            return Response(
                {"password": list(exc.messages)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save(update_fields=["password"])

        return Response({"detail": "Palavra-passe redefinida com sucesso."})