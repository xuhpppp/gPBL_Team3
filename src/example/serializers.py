from rest_framework import serializers

from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
<<<<<<< HEAD
        fields = ('name', 'age', 'address', 'phone_number', 'email', 'id_company', 'id')
=======
        fields = ('name', 'age', 'address', 'phone_number', 'email', 'id_company' , 'id')
>>>>>>> namntd
