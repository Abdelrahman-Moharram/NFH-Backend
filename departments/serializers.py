from rest_framework import serializers
from .models import *
from reports.serializers import ReportDetailsSeriail
from core.services import generate_unique_error_message
from project.regex_repo import departmentNameRegex
import re

from django.db.models import CharField
from django.db.models.functions import Lower

CharField.register_lookup(Lower)



class DepartmentFormSerializer(serializers.ModelSerializer):
    # order       = serializers.IntegerField()
    class Meta:
        model   = Department
        fields  = [
            'name',
            'ar_name',
            # 'icon',
            'color',
            # 'order'
        ]
    @property
    def is_update(self):
        return self.instance is not None
    
    
    

    def validate_name(self, value):
        if Department.objects.filter(name__lower=value.lower()) and not self.is_update:
            raise serializers.ValidationError(generate_unique_error_message(lang=self.context['lang'], ar_name='اسم القسم', name='Department Name'))
        
        if not re.fullmatch(departmentNameRegex['pattern'], value):
            raise serializers.ValidationError(departmentNameRegex['message_ar']if self.context['lang'] == 'ar' else departmentNameRegex['message'])

        return value
    
    def save(self, **kwargs):
        if not self.is_update:
            self.order =  kwargs['order']
        
        return super().save(**kwargs)
    
class BaseDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Department
        fields  = [
            'name',
            'ar_name',
            'icon',
            'color',
            'order'
        ]

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
        repr['icon']                = instance.icon.url
        repr['description']         = instance.name
        repr['color']               = instance.color

        return repr

class DepartmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
    
    def to_representation(self, instance):
        report_details              = ReportDetailsSeriail(instance.reports.all(), many=True)
        repr = dict()
        repr['label']               = instance.name
        # repr['description']         = instance.description
        repr['icon']                = instance.icon.url
        repr['color']               = instance.color

        repr['charts']              = report_details.data

        return repr