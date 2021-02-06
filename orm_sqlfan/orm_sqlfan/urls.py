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
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path,include

from rest_framework.routers import DefaultRouter
#from libreria.views import editorial_detail


from libreria import views
from libreria.views import EditorialExplicitoViewSet, EditorialCortoViewSet,EditorialSoloLecturaViewSet
#from libreria.views import EditorialViewSet,LibroViewSet


# Creamos un router y registramos nuestros viewsets, en este caso solo uno
router = DefaultRouter()
router.register(r'editorial_explicito', EditorialExplicitoViewSet, basename='editorialexp')
router.register(r'editorial_corto', EditorialCortoViewSet, basename='editorialcorto')
router.register(r'editorial_lectura', EditorialSoloLecturaViewSet, basename='editoriallectura')



#router.register(r'editoriales', editorial_detail)
#router.register(r'editoriales', EditorialViewSet)
#router.register(r'libros', LibroViewSet)


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    #path('editorial/', views.editorial_list),
    path('editorial/', views.EditorialLista.as_view()),
    path('editorial/<int:pk>', views.editorial_detail, name='editorial-detail'),
    path('editorial_mixin/', views.EditorialListAPIView.as_view()),
    path('editorial_mixin/<int:pk>', views.EditorialDetailAPIView.as_view()),
    path('editorial_generic/', views.EditorialCreateListView.as_view()),
    path('editorial_GetDeletPutAPIView/<int:pk>', views.EditorialGetDeletePutListView.as_view()),
    path('editorial_ListCreateAPIView/', views.EditorialListCreateAPIView.as_view()),
    path('editorial_PersonalizadoView/<str:buscar>', views.EditorialPersonalizadoView.as_view()),
    path('api/', include(router.urls)),
    # Format .json .api
]



# if settings.DEBUG:
#     import debug_toolbar

#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]
