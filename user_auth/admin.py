from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_type', 'username', 'age', 'can_be_contacted', 'can_data_be_shared')

    def user_type(self, obj):
        return "Admin" if obj.is_staff else "Utilisateur"

    user_type.short_description = "Type d'Utilisateur"
    # refresh_access_token.short_description = "Rafraichir access_token des utilisateurs selectionnés"


admin.register(User, CustomUserAdmin)
