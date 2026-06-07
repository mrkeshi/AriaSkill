"""
URL configuration for Aria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import (
    TokenRefreshView
)


urlpatterns = [
                  path('admin/', admin.site.urls),
                  # Swagger endpoints:
                  path('api/schema/', SpectacularJSONAPIView.as_view(), name='schema'),
                  path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
                  path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                  path('api/account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/account/', include('accounts.urls')),
                  path('api/project/', include('projects.urls')),
                  path('api/activities/', include('activity.urls')),
                  path('api/notifications/', include('notification.urls')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
