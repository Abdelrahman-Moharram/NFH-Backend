from reports.models import ChartAxis, Chart, Report
import pandas as pd
import MySQLdb
from rest_framework.response import Response
from rest_framework import status

def connect_to_mysql(confs):
    
    try:
        conn = MySQLdb.Connection(
            host=confs.ip,
            user=confs.username,
            password=confs.password,
            port=int(confs.port),
            db=confs.schema
        )
    except:
        return None

    return conn.cursor(MySQLdb.cursors.DictCursor)

    
def create_cursor(confs):

    if confs.connection_type == 'oracle':
        return connect_to_mysql(confs=confs)

    elif confs.connection_type == 'mysql':
        return connect_to_mysql(confs=confs)
    
    return None



def data_to_chart_data(chart_id):
    x_cols = ChartAxis.objects.filter(chart__id=chart_id, axis='x').first()
    if not x_cols:
        return []
    
    x_cols = x_cols.name

    
    y_cols = [i[0] for i in ChartAxis.objects.filter(chart__id=chart_id, axis='y').values_list('name')]



    if len(y_cols) == 0:
        return []

    datasets        = []
    chart           = Chart.objects.filter(id=chart_id).first()
    data, errors    = get_chart_data(query=chart.query, report_id=chart.report.id)
    if errors:
        return errors



    df              = pd.DataFrame(data)
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
        return [], {'error':f'this report is not found'}
    
    cursor      = create_cursor(confs=report.connection)


    
    if not cursor :
        return [], {'error':'invalid database credentials'}
    

    try:
        cursor.execute(query)
    except:
        return [], {'query':['this query is invalid, please try a different one']}
    
    
    return [desc[0] for desc in cursor.description], None


def get_chart_data(query, report_id):
    report = Report.objects.filter(id=report_id).first()

    if not report:
        return [], {'error':f'this report is not found'}
    
    cursor      = create_cursor(confs=report.connection)

    if not cursor :
        return [], {'error':'invalid database credentials'}


    try:
        cursor.execute(query)
    except:
        return [], {'query':'this query is invalid, please try a different one'}
    
    return cursor.fetchall(), None