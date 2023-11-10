from django.conf import settings
from django.db import models
from django.utils import timezone
from user_auth.models import User
import uuid


class Project(models.Model):
    PROJECT_TYPES = (
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_projects')
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contributed_projects', blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def add_contributor(self, user):
        self.contributors.add(user)

    def update_updated_time(self):
        self.updated_time = timezone.now()
        self.save()


class Issue(models.Model):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    TO_DO = 'TO DO'
    IN_PROGRESS = 'IN PROGRESS'
    FINISHED = 'FINISHED'
    STATUS_CHOICES = [
        (TO_DO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
    ]

    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'
    TAG_CHOICES = [
        (BUG, 'Bug'),
        (FEATURE, 'Feature'),
        (TASK, 'Task'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_issues')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default=BUG)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='issued_assignee')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=TO_DO)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_comment')
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Commentaire du problème: {self.issue.title}'
