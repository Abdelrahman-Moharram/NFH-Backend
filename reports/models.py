from django.db import models
from project.models import BaseModel, BaseModelManager
from departments.models import Department

class Report(BaseModel):
    name                = models.CharField(max_length=254)
    department          = models.ForeignKey(Department, related_name='reports', null=True, blank=True, on_delete=models.SET_NULL)
    schema              = models.ForeignKey('Schema', null=True, blank=True, on_delete=models.SET_NULL)

    objects   = BaseModelManager

    def __str__(self):
        return self.name



class Chart(BaseModel):
    choices = [
        ['50%'    , '1/2'  ],
        ['33.33%' , '1/3'  ],
        ['66.66%' , '2/3'  ],
        ['100%'   , 'full' ],
    ]
    chart_type          = models.ForeignKey('ChartType', null=True, blank=True, on_delete=models.SET_NULL)
    report              = models.ForeignKey('Report', related_name='charts', null=True, blank=True, on_delete=models.CASCADE)
    query               = models.TextField(null=True, blank=True)
    width               = models.CharField(max_length=10, default='50%', choices=choices)

    objects   = BaseModelManager

    def __str__(self):
        return f'{str(self.report)} - {str(self.chart_type)}'

class ChartAxis(models.Model):
    choices = [
        ['x', 'x'],
        ['y', 'y'],
    ]
    chart               = models.ForeignKey(Chart, null=True, blank=True, on_delete=models.CASCADE)
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




class Schema(BaseModel):
    name                = models.CharField(max_length=254)
    # connection_type     = models.CharField(max_length=254)

    
    objects    = BaseModelManager

    def __str__(self):
        return self.name



