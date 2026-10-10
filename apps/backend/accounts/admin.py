from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Role, User


class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone_number", "role", "status")


class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"


@admin.register(User)
class AccountAdmin(DjangoUserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    list_display = (
        "username",
        "email",
        "phone_number",
        "role",
        "status",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("role", "status", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Conta da barbearia",
            {"fields": ("phone_number", "role", "status", "created_at", "updated_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "role",
                    "status",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def has_module_permission(self, request):
        return request.user.is_superuser or (
            request.user.is_staff and request.user.role == Role.ADMINISTRADOR
        )

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (
            request.user.is_staff
            and request.user.role == Role.ADMINISTRADOR
            and (obj is None or obj.role == Role.BARBEIRO)
        )

    def has_add_permission(self, request):
        return request.user.is_superuser or (
            request.user.is_staff and request.user.role == Role.ADMINISTRADOR
        )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (
            request.user.is_staff
            and request.user.role == Role.ADMINISTRADOR
            and obj is not None
            and obj.role == Role.BARBEIRO
        )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(role=Role.BARBEIRO)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        if obj is None:
            return self.add_fieldsets
        return (
            (
                None,
                {
                    "fields": (
                        "username",
                        "email",
                        "phone_number",
                        "role",
                        "status",
                        "is_active",
                        "created_at",
                        "updated_at",
                    )
                },
            ),
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and "role" in form.base_fields:
            form.base_fields["role"].choices = [
                (Role.BARBEIRO, "Barbeiro"),
            ]
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.role = Role.BARBEIRO
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)