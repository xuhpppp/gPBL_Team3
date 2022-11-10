from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import exceptions
from rest_framework import status

from .models import Person
from .serializers import PersonSerializer

# Create your views here.


class ListPersonView(APIView):
    def get(self, request, format=None, id=None):
        if id is None:
            person = Person.objects.all()
            serializer = PersonSerializer(person, many=True)
            return Response(serializer.data)
        else:
            try:
                person = Person.objects.get(pk=id)
                serializer = PersonSerializer(person, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except exceptions.ObjectDoesNotExist:
                return Response({'message':'Object does not exist'}, status=status.HTTP_204_NO_CONTENT)
