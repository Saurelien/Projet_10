from user_auth.serializers import UserProfileSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from log_app.models import UserLoginLog

User = get_user_model()


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_age = serializer.validated_data.get('age')

            if user_age is not None:
                # Vérifiez l'âge de l'utilisateur
                if user_age < 15:
                    return Response(
                        {"error": "L'utilisateur doit avoir au moins 15 ans."},
                        status=400
                    )
                elif 15 <= user_age <= 17:
                    # L'utilisateur a entre 15 et 17 ans: can_be_contacted et can_data_be_shared à False
                    serializer.validated_data['can_be_contacted'] = False
                    serializer.validated_data['can_data_be_shared'] = False

            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_to_delete = request.user

        try:
            user_to_delete.delete()
            return Response({'message': 'Votre compte a été supprimé avec succès.'},
                            status=204)
        except Exception as e:
            return Response({'error': 'Une erreur s\'est produite lors de la suppression du compte.'},
                            status=500)


class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK and request.user.is_authenticated:
            user = request.user.is_authenticated
            log_entry = UserLoginLog(user=user)
            log_entry.save()

        return response
