from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer

# Create your views here.
class ListPersonView(APIView):
    def get(self, request, format=None):
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        return Response(serializer.data)