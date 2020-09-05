from rest_framework import serializers
from tutor.models import AdsMdmTutor


class TutorSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdsMdmTutor
        fields = '__all__'
