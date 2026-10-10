
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    CLIENTE = "CLIENTE", "Cliente"
    BARBEIRO = "BARBEIRO", "Barbeiro"
    ADMINISTRADOR = "ADMINISTRADOR", "Administrador"


class StatusUser(models.TextChoices):
    ATIVO = "ATIVO", "Ativo"
    INATIVO = "INATIVO", "Inativo"
    BLOQUEADO = "BLOQUEADO", "Bloqueado"


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = models.CharField(
        max_length=150,
        unique=True,
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    phone_number = models.CharField(
        max_length=9,
        unique=True,
    )

    role = models.CharField(
        max_length=14,
        choices=Role.choices,
        default=Role.CLIENTE,
    )

    status = models.CharField(
        max_length=10,
        choices=StatusUser.choices,
        default=StatusUser.ATIVO,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    def __str__(self):
        return self.email