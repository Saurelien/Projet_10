from rest_framework import serializers
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password',  'age', 'can_be_contacted', 'can_data_be_shared')

    def save(self):
        self.instance = User.objects.create_user(self.validated_data.pop('username'),
                                                 password=self.validated_data.pop('password'), **self.validated_data)
        return self.instance

