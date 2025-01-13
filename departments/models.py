from django.db import models
from project.models import BaseModel, BaseModelManager


class Department(BaseModel):
    name            = models.CharField(max_length=254)
    ar_name         = models.CharField(max_length=254)
    icon            = models.TextField(null=True, blank=True)

    order           = models.IntegerField()    

    is_active       = models.BooleanField(default=True)

    @property
    def slug(self):
        return self.name.lower().replace(" ", '-')


    objects = BaseModelManager()

    def __str__(self):
        return self.name
    

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

