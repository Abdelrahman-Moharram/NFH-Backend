from rest_framework import status
from rest_framework.response import Response
from .serializers import AddReportSerializer, AddChartSerializer, DepartmentReportsListSeriail
from .models import Report, ChartType, Connection, Chart, ChartAxis
from departments.models import Department
from rest_framework.decorators import api_view
from accounts.permissions import permission_allowed
from .services import get_chart_cols

@api_view(['POST'])
@permission_allowed('permissions.reports.add')
def add_report(request):
    dept_name       = request.POST.get('dept_name', None)
    department      = Department.objects.filter(slug=dept_name).first()

    if not department:
        return Response({'dept_name':[f'{dept_name} Department is not found']}, status=status.HTTP_400_BAD_REQUEST)
    
    report_serializer       = AddReportSerializer(data=request.data, context={'lang':'en'})

    if report_serializer.is_valid():
        report_serializer   = report_serializer.save(department=department)
        
        chart_serialzer     = AddChartSerializer(data=request.data, context={'lang':'en'})
        if chart_serialzer.is_valid():
            chart_serialzer = chart_serialzer.save(report=report_serializer)
    
            return Response({'message':f'Chart "{request.POST.get('name', None)}" added successfully', 'id':report_serializer.id})

        return Response(chart_serialzer.errors, status=status.HTTP_400_BAD_REQUEST)   
        

    return Response(report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_allowed('permissions.reports.add')
def add_report_base_data(request):
    dept_name       = request.POST.get('dept_name', None)
    department      = Department.objects.filter(slug=dept_name).first()

    if not department:
        return Response({'dept_name':[f'{dept_name} Department is not found']}, status=status.HTTP_400_BAD_REQUEST)
    
    report_serializer       = AddReportSerializer(data=request.data, context={'lang':'en'})

    if report_serializer.is_valid():
        report_serializer   = report_serializer.save(department=department)

        return Response({'message':f'Chart "{request.POST.get('name', None)}" added successfully', 'id':report_serializer.id,}, status=status.HTTP_200_OK)
    
    
    return Response(report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_allowed('permissions.reports.add')
def add_report_chart_data(request, report_id):
    report = Report.objects.filter(id=report_id).first()
    if not report:
        return Response({'error':f'this report is not found'}, status=status.HTTP_404_NOT_FOUND)

    chart_serialzer     = AddChartSerializer(data=request.data, context={'lang':'en'})
    if chart_serialzer.is_valid():

        cols_names, err_res = get_chart_cols(query=chart_serialzer.validated_data.get('query', None), report_id=report_id)

        if err_res:
            return Response(err_res, status=status.HTTP_400_BAD_REQUEST)

        chart_serialzer = chart_serialzer.save(report=report)

        return Response({'message':f'Chart saved successfully', 'cols_names':cols_names, 'id':chart_serialzer.id})

    return Response(chart_serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_allowed('permissions.reports.add')
def add_chart_axis(request, chart_id):
    chart       = Chart.objects.filter(id=chart_id).first()

    if not chart:
        return Response({'error':f'this chart is not found'}, status=status.HTTP_404_NOT_FOUND)
    

    x_axis = request.POST.get('x', None)
    y_axes = request.POST.getlist('y', None)
    
    if not x_axis or not y_axes:
        return Response({'error':f'Invalid coordinates for x axis or y axis'}, status=status.HTTP_400_BAD_REQUEST)

    
    x_axis = ChartAxis.objects.create(
            chart = chart,
            name = x_axis,
            axis = 'x'
        )
    x_axis.save()

    for a in y_axes:
        y_axis = ChartAxis.objects.create(
                chart = chart,
                name = a,
                axis = 'y'
            )
        y_axis.save()
    return Response({'message':f'Chart saved successfully', 'id':chart_id})



@api_view(['GET'])
@permission_allowed('permissions.reports.add')
def get_report_chart_cols(request, chart_id):
    chart       = Chart.objects.filter(id=chart_id).first()

    if not chart:
        return Response({'error':f'this chart is not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    cols_names, err_res = get_chart_cols(query=chart.query, report_id=chart.report.id)

    if err_res:
        return Response(err_res, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'cols_names':cols_names}, status=status.HTTP_200_OK)





@api_view(['GET'])
@permission_allowed('permissions.reports.add')
def report_dropdown(request):
    chart_types         = list(ChartType.objects.order_by('name').values('id', 'name', 'ar_name'))
    connections         = list(Connection.objects.order_by('name').values('id', 'name'))

    return Response(
        {
            'chart_types'       : chart_types,
            'connections'       : connections,
        },
        status=status.HTTP_200_OK
    )