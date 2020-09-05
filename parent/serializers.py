from rest_framework import serializers
from parent.models import AdsMdmParent


class ParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdsMdmParent
        fields = '__all__'
