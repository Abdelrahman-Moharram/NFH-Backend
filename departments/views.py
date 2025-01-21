from rest_framework.response import Response
from rest_framework import status
from departments.serializers import *
from .models import *
from rest_framework.decorators import api_view
from accounts.permissions import permission_allowed
from project.helper import data_to_chart_data

@api_view(['GET'])
@permission_allowed('permissions.departments.view')
def department_list(request):
    departments         = Department.objects.filter(is_active=True).order_by('order')
    departments_serial  = DepartmentListSerializer(departments, many=True)

    return Response(
        {
            'departments': departments_serial.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_allowed('permissions.departments.view')
def depratment_details(request, dept_name):
    department          = Department.objects.filter(is_active=True, slug=dept_name).first()
    if not department:
        return Response(
            {
                "error": 'this department is not found or has been deleted'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    departments_serial  = DepartmentDetailsSerializer(department)

    return Response(
        {
            'department'   : departments_serial.data,
            'chart'        : data_to_chart_data('60041fab-4f1d-4da3-84a6-eea814b614b7')
        },
        status=status.HTTP_200_OK
    )