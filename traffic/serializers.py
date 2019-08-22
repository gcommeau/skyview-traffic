from rest_framework import serializers
from traffic.models import *

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        #fields = ('teacher')
        fields = '__all__'

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        #fields = ('family_number')
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        #fields = ('last_name', 'first_name', 'family', 'classroom')
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        #fields = ('checkout_time', 'family', 'checkout_type')
        fields = '__all__'
