from rest_framework import serializers
from .models import Report, Chart
from .services import data_to_chart_data


class DepartmentReportsListSeriail(serializers.ModelSerializer):
    class Meta:
        model = Report
    
    def to_representation(self, instance):
        repr = dict()

        repr['id']                  = instance.id
        repr['name']                = instance.name
        repr['connection']          = str(instance.connection)

        chart = instance.charts.first()
        if chart:
            repr['chart_type']      = str(chart.chart_type)


        return repr



class ReportDetailsSeriail(serializers.ModelSerializer):
    class Meta:
        model = Report
    
    def to_representation(self, instance):
        repr = dict()
        repr['name']                = instance.name
        repr['connection']          = str(instance.connection)
        repr['chart']               = data_to_chart_data(instance.charts.first().id) if instance.charts.exists() else None # TODO -> make serialzer error if data is invalid
        
        return repr


class AddReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report

        fields = [
            'name',
            'connection',
        ]
    @property
    def is_update(self):
        return self.instance is not None
    
    def save(self, *args, **kwargs):
        if not self.is_update:
            self.department =  kwargs['department']
        return super().save(**kwargs)


class AddChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = [
            'chart_type',
            'query',
            # 'width',
        ]
    @property
    def is_update(self):
        return self.instance is not None
    
    
    def save(self, *args, **kwargs):
        if not self.is_update:
            self.report =  kwargs['report']
        return super().save(**kwargs)