from django.http import JsonResponse
from django.views import View
from project_manager.serializers import ProjectSerializer, IssueSerializer, ProjectDetailSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from project_manager.models import Project, Issue, Comment
from rest_framework.exceptions import ValidationError
from project_manager.permissions import IsProjectAuthor, IsIssueCreator, IsCommentAuthor
from libs.views import MultipleSerializerMixin

User = get_user_model()


class ProjectViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    detail_serializer_class = ProjectDetailSerializer
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_queryset(self):
        if self.action == "join":
            return Project.objects.all()
        return self.request.user.contributed_projects.order_by("created_time")

    def perform_create(self, serializer):
        user = self.request.user
        user_age = user.age

        if user_age < 18:
            raise ValidationError({'error': 'Vous devez être majeur pour cette action.'})

        project = serializer.save(author=user)

        # Ajoutez les détails des contributeurs au projet
        project.contributors.set([user])
        project.save()

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        project = self.get_object()
        user = self.request.user

        # Vérifiez si l'utilisateur est déjà contributeur du projet
        if project.contributors.filter(id=user.id).exists():
            # L'utilisateur est déjà contributeur du projet
            return Response({'message': f'Vous avez déjà rejoint le projet {project.title} ID: {project.pk}.'},
                            status=200)

        # Ajoutez l'utilisateur en tant que contributeur
        project.contributors.add(user)
        return Response({'message': 'Inscription au projet réussie.'}, status=200)


class ProjectJSONView(View):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            # Obtenez la liste des noms d'utilisateur des contributeurs
            contributor_usernames = [contributor.username for contributor in project.contributors.all()]
            project_data = {
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'type': project.type,
                'author': project.author.username,
                'contributors': contributor_usernames,
                'created_time': project.created_time.astimezone(timezone.get_current_timezone())
                .strftime("%d-%m-%Y %H:%M"),
            }
            return JsonResponse(project_data)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Projet non trouvé'}, status=404)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsIssueCreator]

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributors=user, project__id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, project_id=self.kwargs["project_pk"])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsCommentAuthor]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
