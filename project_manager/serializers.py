from user_auth.models import User
from rest_framework import serializers
from project_manager.models import Project, Issue, Comment


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared')


class ProjectDetailSerializer(serializers.ModelSerializer):
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('pk', 'title', 'description', 'type', 'contributors', 'created_time', 'updated_time')

    def get_contributors(self, obj):
        # Renvoye une liste des noms d'utilisateur des contributeurs
        return UserDetailSerializer(obj.contributors.all(), many=True).data


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('pk', 'title', 'description', 'type', 'created_time', 'updated_time')

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise serializers.ValidationError("Le titre du projet existe déjà")
        return value


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = (
            'pk', 'title', 'description', 'assignee', 'status', 'priority', 'tag',
            'created_time', 'updated_time'
        )
        read_only_fields = ('created_time', 'updated_time')

    def validate_assignee(self, value):
        if value is not None:
            project_pk = self.context["view"].kwargs["project_pk"]
            if not value.contributed_projects.filter(pk=project_pk).exists():
                raise serializers.ValidationError('L\'utilisateur assigné doit être un contributeur du projet.')

            return value

        return self.context['request'].user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'description', 'issue', 'created_time', 'updated_time')

    def validate_issue(self, value):
        user = self.context['request'].user
        project = value.project
        if not project.contributors.filter(id=user.id).exists():
            raise serializers.ValidationError('Vous n\'êtes pas autorisé à répondre à cette issue.')

        return value
