from django.contrib import admin
from .models import *

admin.site.register(Role)
admin.site.register(Module)
admin.site.register(Permission)
admin.site.register(Role_Permission)

# Register your models here.
