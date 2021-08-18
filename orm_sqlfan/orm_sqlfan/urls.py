"""orm_sqlfan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from libreria import views
from rest_framework.authtoken import views as view_auth
from knox import views as knox_views
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from knox.auth import TokenAuthentication

import debug_toolbar

class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/',include('libreria.urls')),
    path('api_authorization/', include('rest_framework.urls')),
    path('api-token-auth-custom/',views.CustomAuthToken.as_view()),
    path('api-token/', view_auth.obtain_auth_token),
    path('auth-djoser/', include('djoser.urls')),
    path('auth-djoser/', include('djoser.urls.authtoken')),
    path('api/activate/<str:uid>/<str:token>/', views.ActivateUserByGet.as_view(), name='user-activate'),

    path('knox/login/', LoginView.as_view(), name='knox_login'),
    path('knox/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('knox/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
