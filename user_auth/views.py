from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models

class Inscription(APIView):
    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utilisateur = serializer.save()
        refresh = RefreshToken.for_user(utilisateur)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class Connexion(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        utilisateur = authenticate(email=email, password=password)
        if utilisateur:
            refresh = RefreshToken.for_user(utilisateur)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Identifiants invalides.'}, status=400)
