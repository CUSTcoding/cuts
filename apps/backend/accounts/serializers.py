
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[])
    email = serializers.EmailField(validators=[])
    phone_number = serializers.CharField(validators=[])

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )

    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "created_at",
            "updated_at",
            "password",
            "password_confirm",
            "access",
            "refresh",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "access",
            "refresh",
        ]

    def validate_email(self, value):
        return value.lower()

    def validate_phone_number(self, value):
        second = ["2", "3", "4", "5", "6", "7"]

        if (
            not value.isdigit()
            or len(value) != 9
            or not value.startswith("8")
            or value[1] not in second
        ):
            raise serializers.ValidationError(
                "O número deve ter 9 dígitos e começar por "
                "82, 83, 84, 85, 86 ou 87."
            )

        return value

    def validate_username(self, value):
        return value

    def validate(self, attrs):
        email_exists = User.objects.filter(
            email__iexact=attrs["email"]
        ).exists()
        username_exists = User.objects.filter(
            username__iexact=attrs["username"]
        ).exists()
        phone_exists = User.objects.filter(
            phone_number=attrs["phone_number"]
        ).exists()

        if email_exists or username_exists or phone_exists:
            raise serializers.ValidationError(
                "Não foi possível criar a conta com os dados fornecidos."
            )

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "As palavras-passe não coincidem."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)

        user.access = str(refresh.access_token)
        user.refresh = str(refresh)

        return user

class LoginSerializer(TokenObtainPairSerializer):
    username_field = "identifier"

    identifier = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        user = (
            User.objects.filter(email__iexact=identifier).first()
            or User.objects.filter(phone_number=identifier).first()
        )
    
        if not user:
            raise serializers.ValidationError({
                "detail": "Credentials are not valid.",
                "code": "authorization",
            })

        authenticated_user = authenticate(
            request=self.context.get("request"),
            username=user.email,
            password=password,
        )

        if (
            not authenticated_user
            or authenticated_user.pk != user.pk
            or not authenticated_user.is_active
            or authenticated_user.status != "ATIVO"
        ):
            raise serializers.ValidationError({
                "detail": "Credentials are not valid or account is inactive.",
                "code": "authorization",
            })

        self.user = authenticated_user

        refresh = self.get_token(authenticated_user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number"]

    def validate_email(self, value):
        value = value.lower()

        if User.objects.filter(
            email__iexact=value
        ).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError(
                "Este email já está registado."
            )

        return value

    def validate_username(self, value):
        if User.objects.filter(
            username__iexact=value
        ).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError(
                "Este username já está registado."
            )

        return value

    def validate_phone_number(self, value):
        second = ["2", "3", "4", "5", "6", "7"]

        if (
            not value.isdigit()
            or len(value) != 9
            or not value.startswith("8")
            or value[1] not in second
        ):
            raise serializers.ValidationError(
                "Número de telefone inválido."
            )

        if User.objects.filter(
            phone_number=value
        ).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError(
                "Este número já está registado."
            )

        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({
                "old_password": "A palavra-passe atual está incorreta."
            })

        if attrs["new_password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "As palavras-passe não coincidem."
            })

        validate_password(attrs["new_password"], user=user)

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user