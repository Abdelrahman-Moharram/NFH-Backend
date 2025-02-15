from rest_framework import serializers
from .models import Report, Chart, Connection
from .services import data_to_chart_data, check_db_connection
from datetime import datetime, timezone
import re
from project.regex_repo import domainRegex, portNumberRegex
class DepartmentReportsListSeriail(serializers.ModelSerializer):
    class Meta:
        model = Report
    
    def to_representation(self, instance):
        repr = dict()

        repr['id']                  = instance.id
        repr['name']                = instance.name
        repr['connection']          = str(instance.connection)

        chart = instance.chart
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
        repr['chart']               = data_to_chart_data(instance.chart.id) if instance.chart else None # TODO -> make serialzer error if data is invalid
        
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



class GetChartFormData(serializers.ModelSerializer):
    class Meta:
        model = Report
        
    
    def to_representation(self, instance):
        repr = dict()
        repr['name']                    = instance.name
        repr['connection']              = instance.connection.id
        repr['chart_type']              = instance.chart.chart_type.id
        repr['query']                   = instance.chart.query
        repr['width']                   = instance.chart.width

        x_axis = instance.chart.x_axis
        if x_axis:
            repr['x_axis']              = x_axis.name
        
        repr['y_axes']                  = [i.name for i in instance.chart.y_axes]


        return repr

    
    
class ConnectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            'id',
            'name',
            'ip',
            'port',
            'schema',
            'username',
            'connection_type',
        ]
    
    def to_representation(self, instance):
        repr = dict()
        
        repr['id']                  = instance.id
        repr['Name']                = instance.name
        repr['IP Address']          = instance.ip
        repr['Port']                = instance.port
        repr['Schema']              = instance.schema
        repr['Username']            = instance.username
        repr['Connection Type']     = instance.connection_type
        repr['Is Connected']        = "Yes" if check_db_connection(instance) else 'No'

        return repr
    

class ConnectionFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            'name',
            'ip',
            'port',
            'schema',
            'username',
            'password',
            'connection_type',
        ]
    @property
    def is_update(self):
        return self.instance is not None
    
    def validate_port(self, value):
        if not re.fullmatch(portNumberRegex['pattern'], str(value)):
            raise serializers.ValidationError(portNumberRegex['message_ar']if self.context['lang'] == 'ar' else portNumberRegex['message'])
        
        return value
    
    def validate_ip(self, value):
        if not re.fullmatch(domainRegex['pattern'], value):
            raise serializers.ValidationError(domainRegex['message_ar']if self.context['lang'] == 'ar' else domainRegex['message'])
        
        return value

    def save(self, *args, **kwargs):
        if self.is_update:
            self.updated_by     =  kwargs['created_by']
            self.last_update_at =  datetime.now(tz=timezone.utc)
        return super().save(**kwargs)
