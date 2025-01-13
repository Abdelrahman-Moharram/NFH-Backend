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
