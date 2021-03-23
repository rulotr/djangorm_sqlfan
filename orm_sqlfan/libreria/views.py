from django.shortcuts import render

from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def editorial_detail(request, pk):
    if request.method == 'GET':
        return Response('Vista de la Editorial')