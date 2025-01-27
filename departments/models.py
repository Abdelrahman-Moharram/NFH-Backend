from django.db import models
from project.models import BaseModel, BaseModelManager
from django.utils.text import slugify



class Department(BaseModel):
    name                = models.CharField(max_length=254)
    ar_name             = models.CharField(max_length=254)
    icon                = models.FileField(upload_to='departments/icons/')
    color               = models.CharField(max_length=10, default='#000')
    order               = models.IntegerField()    
    is_active           = models.BooleanField(default=True)

    slug                = models.SlugField(max_length=255, unique=True, blank=True) 


    objects = BaseModelManager()

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

