from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from project_manager.models import Project, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'type', 'author', 'created_time', 'view_as_json_link', 'contributors_list', 'updated_time')
    list_filter = ('type', 'author')
    search_fields = ('title', 'author__username')

    def view_as_json_link(self, obj):
        url = reverse('project-json', args=[obj.id])
        return format_html('<a href="{}" target="_blank">Voir JSON</a>', url)
    view_as_json_link.short_description = 'JSON Project'

    def contributors_list(self, obj):
        return ", ".join([user.username for user in obj.contributors.all()])
    contributors_list.short_description = 'Contributeurs'

    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression des projets par l'administrateur
        return False

    def has_view_permission(self, request, obj=None):
        # Vérifiez si l'utilisateur est un superutilisateur
        return request.user.is_superuser


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'author', 'assignee', 'status', 'created_time', 'updated_time')
    list_filter = ('project', 'status')
    search_fields = ('title', 'description')
    readonly_fields = ('created_time', 'updated_time')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('uid', 'author', 'issue', 'created_time', 'updated_time')
    list_filter = ('issue', 'created_time', 'updated_time')
    search_fields = ('author__username', 'issue__title', 'description')


# Enregistrez la classe personnalisée dans l'administration
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue)
admin.site.register(Comment, CommentAdmin)
