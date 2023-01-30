from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class HomePage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'paginas/index.html'

    def get(self, request):
        return Response({'nombre_catalogo': "Catalogo de Libros"})


class HomePageAutor(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'paginas/autor.html'

    def get(self, request):
        return Response({'nombre_catalogo': "Catalogo de Autores"})
    