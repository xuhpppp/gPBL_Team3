from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
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
        serializer = PersonSerializer(data=request.data)
        try:
             person = Person.objects.all()
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND )
        if request.methot =='DELETE':
            operation = Person.delete()
            data = {}
            if operation:
                data["success"] = "delete successful"
            else:
                data["failure"] = "delete failed"
            return Response(data=data)
