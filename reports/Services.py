from reports.models import ChartAxis, Chart, Report
import pandas as pd
import MySQLdb
from rest_framework.response import Response
from rest_framework import status


def data_to_chart_data(chart_id):
    # x_cols = 'RECEIVABLES'
    x_cols = ChartAxis.objects.filter(chart__id=chart_id, axis='x').first().name

    # y_cols = ['BUCKET_1', 'BUCKET_2', 'BUCKET_3', 'BUCKET_4', 'BUCKET_5', 'BUCKET_6']
    y_cols = [i[0] for i in ChartAxis.objects.filter(chart__id=chart_id, axis='y').values_list('name')]

    
    datasets    = []
    chart       = Chart.objects.filter(id=chart_id).first()
    df          = pd.DataFrame(get_chart_data(query=chart.query, report_id=chart.report.id))


    for col in y_cols:
        axis = ChartAxis.objects.filter(chart=chart, name=col).first()
        if axis and axis.axis == 'y':
            datasets.append({
                'yAxisID'           : 'y',
                'label'             : axis.name,
                'borderColor'       : axis.color,
                'backgroundColor'   : axis.color,
                'data'              : list(df[col]),
            })
    data = {
        'data' : {
            'labels': list(df[x_cols]),
            'datasets': datasets
        },
        'options':{
            'type'  : str(chart.chart_type),
            'width' : chart.width
        }
        
    }

    return data


def get_chart_cols(query, report_id):
    report = Report.objects.filter(id=report_id).first()

    if not report:
        return [], Response({'error':f'this report is not found'}, status=status.HTTP_404_NOT_FOUND)
    
    confs  = report.connection

    try:
        conn = MySQLdb.Connection(
            host=confs.ip,
            user=confs.username,
            passwd=confs.password,
            port=int(confs.port),
            db=confs.schema
        )
    except:
        return [], Response({'error':'invalid database credentials'}, status=status.HTTP_400_BAD_REQUEST)

    cursor = conn.cursor()

    try:
        cursor.execute(query)
    except:
        return [], Response({'query':'this query is invalid, please try a different one'}, status=status.HTTP_400_BAD_REQUEST)
    
    return [desc[0] for desc in cursor.description], None

def get_chart_data(query, report_id):
    report = Report.objects.filter(id=report_id).first()

    if not report:
        return [], Response({'error':f'this report is not found'}, status=status.HTTP_404_NOT_FOUND)
    
    confs  = report.connection

    try:
        conn = MySQLdb.Connection(
            host=confs.ip,
            user=confs.username,
            passwd=confs.password,
            port=int(confs.port),
            db=confs.schema
        )
    except:
        return [], Response({'error':'invalid database credentials'}, status=status.HTTP_400_BAD_REQUEST)

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute(query)
    except:
        return [], Response({'query':'this query is invalid, please try a different one'}, status=status.HTTP_400_BAD_REQUEST)
    
    return cursor.fetchall()