from django.db import models
from project.models import BaseModel, BaseModelManager
from core.models import Schema, ChartType, Status
from departments.models import Department


class Report(BaseModel):
    name                = models.CharField(max_length=254)
    query               = models.TextField(null=True, blank=True)

    department          = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    
    schema              = models.ForeignKey(Schema, null=True, blank=True, on_delete=models.SET_NULL)
    chart_type          = models.ForeignKey(ChartType, null=True, blank=True, on_delete=models.SET_NULL)


    status              = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)


    objects   = BaseModelManager


