from django.urls import path
from .views import *
app_name = 'reports'
urlpatterns = [
    path("add/", add_report, name="add_report"),
    path("add/base-data/", add_report_base_data, name="add_report_base_data"),
    path("add/chart-data/<str:report_id>/", add_report_chart_data, name="add_report_chart_data"),
    
    path("charts/<str:chart_id>/cols/", get_report_chart_cols, name="get_report_chart_cols"),
    path("charts/<str:chart_id>/axis/add/", add_chart_axis, name="add_chart_axis"),

    path("form-dropdowns/", report_dropdown, name="report_dropdown"),
]
