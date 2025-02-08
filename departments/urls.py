from django.urls import path
from .views import *

app_name = 'departments'

urlpatterns = [
    path("", department_list, name="department_list"),
    path("add/", add_department, name="add/add_department"),
    path("<str:dept_name>/", depratment_details, name="depratment_details"),
    path("<str:dept_name>/reports/", depratment_reports, name="depratment_reports"),
    path("edit/<str:dept_name>/", Department_Details.as_view(), name="depratment_details"),
]
