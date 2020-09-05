from rest_framework import serializers
from student.models import AdsMdmStudent


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdsMdmStudent
        fields = '__all__'
