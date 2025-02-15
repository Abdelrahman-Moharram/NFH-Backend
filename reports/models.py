from django.db import models
from project.models import BaseModel, BaseModelManager
from departments.models import Department
from project.helper import get_connection_types_as_choices_list


class Report(BaseModel):
    name                = models.CharField(max_length=254)
    department          = models.ForeignKey(Department, related_name='reports', null=True, blank=True, on_delete=models.SET_NULL)
    connection          = models.ForeignKey('Connection', on_delete=models.CASCADE)

    objects   = BaseModelManager

    def __str__(self):
        return self.name



class Chart(BaseModel):
    choices = [
        ['50%'    , '1/2'  ],
        ['100%'   , 'full' ],
    ]
    chart_type          = models.ForeignKey('ChartType', on_delete=models.CASCADE)
    report              = models.OneToOneField('Report', related_name='chart', on_delete=models.CASCADE)
    query               = models.TextField()
    width               = models.CharField(max_length=10, default='50%', choices=choices)

    objects   = BaseModelManager

    @property
    def x_axis(self):
        return ChartAxis.objects.filter(axis='x', chart=self).first()
    
    @property
    def y_axes(self):
        return ChartAxis.objects.filter(axis='y', chart=self)

    def __str__(self):
        return f'{str(self.report)} - {str(self.chart_type)}'

class ChartAxis(models.Model):
    choices = [
        ['x', 'x'],
        ['y', 'y'],
    ]
    chart               = models.ForeignKey(Chart, related_name='axes', null=True, blank=True, on_delete=models.CASCADE)
    name                = models.CharField(max_length=80)
    axis                = models.CharField(max_length=10, choices=choices)
    color               = models.CharField(max_length=10, default='#000')

    def __str__(self):
        return self.name + f' - ({self.axis})' 



class ChartType(BaseModel):
    name                = models.CharField(max_length=50)
    ar_name             = models.CharField(max_length=50, null=True, blank=True)   

    description         = models.TextField(null=True, blank=True)
    ar_description      = models.TextField(null=True, blank=True)
    
    
    
    objects    = BaseModelManager
    def __str__(self):
        return self.name







class Connection(BaseModel):

    connection_type     = models.CharField(null=True, blank=True, max_length=20, choices=get_connection_types_as_choices_list(), default='oracle')
    name                = models.CharField(max_length=100)
    ip                  = models.CharField(max_length=50)
    port                = models.IntegerField()
    schema              = models.CharField(max_length=100)
    username            = models.CharField(max_length=200)
    password            = models.CharField(max_length=254) # encrypt password on saving in db
    
    objects    = BaseModelManager

    class Meta:
        unique_together = (
            'connection_type',
            'ip',
            'port',
            'schema',
        )
        

    def __str__(self):
        return f'{self.ip}:{self.port}/{self.schema}'



