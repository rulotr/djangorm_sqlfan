from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


# Create your views here.
class HomePage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pages/index.html'

    def get(self, request):
        return Response()

class HomePageWithAlpine(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pages/indexWithAlpine.html'

    def get(self, request):
        return Response()