from django.urls import path, include
from libreria import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vc_editorial', views.EditorialViewSet,
                basename='vc_editorial')
router.register(r'vcm_editorial', views.EditorialCortoViewSet)
router.register(r'vcsl_editorial', views.EditorialSoloLecturaViewSet)
router.register(r'vclr_editorial', views.CreateListRetrieveViewSet)
router.register(r'usuarios', views.UsuariosVista)

urlpatterns = [
    path('fv_editorial_falsa/<int:pk>',
         views.fv_editorial_falsa, name='fv_editorial-falsa'),
    path('fv_editoriales/', views.fv_editorial_lista, name='fv_editorial-lista'),
    path('fv_editoriales/<int:pk>', views.fv_editorial_detalle,
         name='fv_editorial-detalle'),
    path('fv_libros/', views.fv_libro_lista, name='fv_libro-tipos'),
    path('cv_autores/', views.AutorApiView.as_view(), name='cv_autores'),
    # path('cv_autores_detalle/<int:pk>', views.AutorDetalleApiView.as_view(),
    #     name = 'cv_autores_detalle'),

    path('cv_editoriales/', views.EditorialListaApiView.as_view(),
         name='cv_editoriales'),
    path('cv_editoriales/<int:pk>', views.EditorialDetalleApiView.as_view(),
         name='cv_editoriales_detalle'),
    path('cg_editoriales/', views.EditorialListaGenericApiView.as_view(),
         name='cg_editoriales'),
    path('cg_editoriales/<int:pk>', views.EditorialDetalleGenericApiView.as_view(),
         name='cg_editoriales_detalle'),
    path('cc_editoriales/', views.EditorialListaConcretaGenericApiView.as_view(),
         name='cc_editoriales_detalle'),
    path('cp_editoriales/', views.EditorialListaCustomApiView.as_view(),
         name='cp_editoriales_detalle'),
    path('cp_libros/', views.LibroListaCustomApiView.as_view(), name='cp_libros'),
    path('vistas/', include(router.urls)),
    path('cf_libros/', views.LibroConFiltros.as_view(), name='cf_libros'),
    path('cf_libros_agrupados/', views.LibroConFiltroAgrupado.as_view(),
         name='cf_libros_agrupados'),

    path('ex_editorial/', views.EditorialListaConExcepciones.as_view(),
         name='ex_editorial'),
    path('imagen_editorial_json/', views.EditorialImagenJson.as_view(),
         name='imagen_editorial_json'),
    path('imagen_editorial_htmlform/', views.EditorialImagenMultiParser.as_view(),
         name='imagen_editorial_htmlform'),
    path('imagen_editorial_imagen/<str:filename>',
         views.EditorialImagenFileUploadParser.as_view(), name='imagen_editorial_imagen'),
    path('imagen_editorial_borrar/<int:pk>',
         views.EditorialBorrarImagen.as_view(), name='imagen_editorial_borrar'),

    path('cv_autor_con_calificaciones/',
         views.AutorConCalificacionesApiView.as_view(), name='cv_autor_con_calificaciones'),

]
