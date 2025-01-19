from rest_framework import serializers
from .models import *

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Department
        fields  = [
            'name',
            'ar_name',
            'order',
            'slug',
            'icon'
        ]
    
    def to_representation(self, instance):
        repr                        = dict()

        repr['label']               = instance.name
        repr['href']                = instance.slug
        repr['icon']                = instance.icon
        repr['description']         = instance.name
        repr['color']               = instance.color

        return repr
