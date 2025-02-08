from django.contrib import admin
from .models import *


admin.site.register(Report)
admin.site.register(Chart)
admin.site.register(ChartAxis)
admin.site.register(ChartType)
admin.site.register(Connection)