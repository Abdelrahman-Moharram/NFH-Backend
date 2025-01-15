from rest_framework.response import Response
from rest_framework import status
from departments.serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from accounts.permissions import permission_allowed


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

