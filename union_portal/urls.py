"""
URL configuration for union_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # Добавляем маршруты для наших приложений
    path('', include('apps.news.urls', namespace='news')),
    path('members/', include('apps.members.urls', namespace='members')),
    path('protocols/', include('apps.protocols.urls', namespace='protocols')),
    path('voting/', include('apps.voting.urls', namespace='voting')),
    path('finance/', include('apps.finance.urls', namespace='finance')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('auth/', include('apps.authentication.urls', namespace='auth')),
]

# Обслуживание медиафайлов при разработке
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
