from django.shortcuts import render

# Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def editorial_detail(request, pk):
    if request.method == 'GET':
        return Response('Vista de la Editorial')