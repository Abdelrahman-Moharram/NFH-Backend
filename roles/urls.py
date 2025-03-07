from django.urls import path
from .views import *

app_name = 'roles'

urlpatterns = [
    path("", list_roles, name="list_roles"),
    path("add/", add_role, name="add_role"),
    path("<str:id>/", role_details, name="role_details"),
    path("<str:id>/form-data/", role_form_data, name="role_details"),
    path("<str:id>/edit/", edit_role, name="edit_role"),
    path("<str:id>/add-permission/", add_permission_to_role, name="add_permission_to_role"),
]
