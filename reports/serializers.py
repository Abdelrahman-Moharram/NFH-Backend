from rest_framework import serializers
from .models import Report
from .services import data_to_chart_data


class ReportDetailsSeriail(serializers.ModelSerializer):
    class Meta:
        model = Report
    
    def to_representation(self, instance):
        repr = dict()

        repr['name']                = instance.name
        repr['schema']              = str(instance.schema)


        repr['chart']              = data_to_chart_data(instance.charts.first().id) if instance.charts.exists() else None


        return repr