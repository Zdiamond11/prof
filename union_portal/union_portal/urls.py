"""union_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home, name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('members/', include('members.urls', namespace='members')),
    path('news/', include('news.urls', namespace='news')),
    path('protocols/', include('protocols.urls', namespace='protocols')),
    path('voting/', include('voting.urls', namespace='voting')),
    path('finances/', include('finances.urls', namespace='finances')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('', include('core.urls', namespace='core')),
]