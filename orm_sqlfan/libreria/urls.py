from django.urls import path
from libreria import views

urlpatterns =[
   path('fv_editorial_falsa/<int:pk>', views.fv_editorial_falsa, name='fv_editorial-falsa'),
   path('fv_editoriales/', views.fv_editorial_lista, name='fv_editorial-lista'),
   path('fv_editoriales/<int:pk>', views.fv_editorial_detalle, name='fv_editorial-detalle'),
   path('fv_libros/', views.fv_libro_lista, name='fv_libro-tipos'),
   path('cv_editoriales/', views.EditorialListaApiView.as_view(), name='cv_editoriales'),
   path('cv_editoriales/<int:pk>', views.EditorialDetalleApiView.as_view(), name='cv_editoriales_detalle'),

 ]

