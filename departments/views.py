from rest_framework.response import Response
from rest_framework import status
from departments.serializers import *
from .models import *
from rest_framework.decorators import api_view
from accounts.permissions import permission_allowed
from rest_framework.views import APIView
from reports.serializers import DepartmentReportsListSeriail


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
            # 'chart'        : data_to_chart_data('60041fab-4f1d-4da3-84a6-eea814b614b7')
        },
        status=status.HTTP_200_OK
    )




@api_view(['GET'])
@permission_allowed('permissions.reports.add')
def depratment_reports(request, dept_name):
    
    department          = Department.objects.filter(is_active=True, slug=dept_name).first()
    if not department:
        return Response(
            {
                "error": 'this department is not found or has been deleted'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    reports_serial  = DepartmentReportsListSeriail(department.reports, many=True)

    return Response(
        {
            'reports': reports_serial.data,
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_allowed('permissions.departments.add')
def add_department(request):
        


        serializer      = DepartmentFormSerializer(data=request.data, context={'lang':'en'})
        

        if serializer.is_valid():
            icon            = request.FILES.get('icon', None)
            if not icon:
                return Response({'icon':['icon is required or invalid file format']}, status=status.HTTP_400_BAD_REQUEST)
            

            order  = Department.objects.latest('order').order+1 if Department.objects.count() else 1
            serializer  = serializer.save(order=order)
            
            serializer.icon = icon
            serializer.save()
            return Response({'message':f'Department "{request.POST.get('name', None)}" added successfully', 'slug':serializer.slug})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Department_Details(APIView):

    def get(self, request, dept_name, format=None):
        department      = Department.objects.filter(slug=dept_name).first()
        serializer      = BaseDepartmentSerializer(department)

        return Response(
            {
                'department':serializer.data
            }, 
            status=status.HTTP_200_OK
        )
    
    def put(self, request, dept_name, format=None):
        department      = Department.objects.filter(slug=dept_name).first()
        serializer      = DepartmentFormSerializer(department, data=request.data, context={'lang':'en'})
        icon            = request.FILES.get('icon', None)



        if serializer.is_valid():
            serializer = serializer.save()

            if icon:
                serializer.icon = icon
                serializer.save()
            
            return Response({'message':f'Department "{request.POST.get('name', None)}" saved successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)