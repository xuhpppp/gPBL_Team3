from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core import exceptions

from .models import Person
from .serializers import PersonSerializer

# Create your views here.
class ListPersonView(APIView):
    def get(self, request, format=None):
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PersonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new person successfully'
            }, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                'message': 'Create a new person unsuccessfully'
            }, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        person = get_object_or_404(Person, id=kwargs.get('pk'))

        if person is not None:
            person.delete()

            return JsonResponse({
                'message': 'delete 1 person successfully'
            }, status = status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        person = get_object_or_404(Person, id=kwargs.get('pk'))

        if person is not None:
            serializer = PersonSerializer(person, request.data)

            if serializer.is_valid():
                serializer.save()

                return JsonResponse({
                    'message': 'update 1 person successfully'
                }, status = status.HTTP_200_OK)
            else:
                return JsonResponse({
                    'message': 'update 1 person unsuccessfully'
                }, status = status.HTTP_200_OK)
