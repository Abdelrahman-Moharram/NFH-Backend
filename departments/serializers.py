from rest_framework import serializers
from .models import *
from reports.serializers import ReportDetailsSeriail

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
        repr['icon_str']            = instance.icon
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
        repr['icon']                = instance.icon
        repr['color']               = instance.color

        repr['charts']              = report_details.data

        return repr