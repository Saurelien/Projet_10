from user_auth.models import User  # Assurez-vous d'importer le modèle User personnalisé
from django.db import models


class UserLoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
