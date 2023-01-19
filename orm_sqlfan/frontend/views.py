from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class HomePage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'paginas/index.html'

    def get(self, request):
        return Response()