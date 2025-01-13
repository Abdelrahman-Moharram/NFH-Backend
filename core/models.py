from django.db import models
from project.models import BaseModel, BaseModelManager


class Status(models.Model):
    name                = models.CharField(max_length=50)
    ar_name             = models.CharField(max_length=50)


    
    def __str__(self):
        return self.name



class ChartType(BaseModel):
    name                = models.CharField(max_length=50)
    ar_name             = models.CharField(max_length=50)   

    description         = models.TextField(null=True, blank=True)
    ar_description      = models.TextField(null=True, blank=True)
    
    objects    = BaseModelManager
    def __str__(self):
        return self.name

class Schema(BaseModel):
    name            = models.CharField(max_length=254)
    connection_type = models.CharField(max_length=254)

    
    objects    = BaseModelManager

    def __str__(self):
        return self.name