from django.urls import path
from .views import *

app_name = 'departments'

urlpatterns = [
    path("", department_list, name="department_list"),
]
