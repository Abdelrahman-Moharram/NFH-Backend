from django.urls import path
from .views import *

app_name = 'roles'

urlpatterns = [
    path("", list_roles, name="list_roles"),
    path("<str:id>/", role_details, name="role_details"),
]