"""
URL configuration for softdesk_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from user_auth.views import UserRegistrationView, UserDeleteView, CustomTokenObtainPairView, CustomTokenRefreshView
from project_manager.views import ProjectJSONView
from rest_framework_nested import routers
from project_manager.views import ProjectViewSet, IssueViewSet, CommentViewSet

# Création d'un routeur pour gérer les vues de ProjectViewSet
router = routers.SimpleRouter()
router.register(r'project', ProjectViewSet, basename="project")

router_project = routers.NestedSimpleRouter(router, 'project', lookup='project')
router_project.register(r'issue', IssueViewSet, basename="issue")

router_issue = routers.NestedSimpleRouter(router_project, 'issue', lookup='issue')
router_issue.register(r'comment', CommentViewSet, basename="comment")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_auth/register/', UserRegistrationView.as_view(), name='register-user'),
    path('user_auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user_auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('user/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('project/<int:pk>/view_as_json/', ProjectJSONView.as_view(), name='project-json'),
    path('api/', include(router.urls)),
    path('api/', include(router_project.urls)),
    path('api/', include(router_issue.urls)),
]
