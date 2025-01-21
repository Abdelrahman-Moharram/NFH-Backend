from django.urls import path
from .views import *

app_name = 'departments'

urlpatterns = [
    path("", department_list, name="department_list"),
    path("<str:dept_name>/", depratment_details, name="depratment_details"),
]
