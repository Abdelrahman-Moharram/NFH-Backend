from reports.models import ChartAxis, Chart, Report
import pandas as pd
import MySQLdb
import cx_Oracle


charts_options = {
    'bar': 
    {
        'single':{
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': { 'display': False },
                },
            'scales': {
            'x': {
                'display': False, 
            },
            'y': {
                    'display': False,
                    'min': 0,
                    'max': 100, 
                },
            },
            'barPercentage': 0.5, 
            'categoryPercentage': 0.8, 
        },
        'multiple':{
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {'display': False}  # Hide legend
            },
            'scales': {
                'x': {
                    'grid': {'display': False},  # Hide grid lines
                    'ticks': {'color': "#4A5A74", 'font': {'weight': "bold"}}
                },
                'y': {
                    'display': False,  # Hide Y-axis labels
                    'min': 0,
                    'max': 200,  # Ensures space above max value
                    'grid': {'display': False}
                }
            },
            
        }
    },
    'line': {
        'single': {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {'display': False}  # Hide legend
            },
            'scales': {
                'x': {
                    'display': False  # Hide x-axis labels
                },
                'y': {
                    'display': False  # Hide y-axis labels
                }
            }
        },
        'multiple':{
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {'display': False},
                'tooltip': {'enabled': True},
            },
            'scales': {
                'x': {
                    'ticks': {'color': "#061631"},  # White text
                    'grid': {'display': False},
                },
                'y': {
                    'ticks': {'color': "#061631"},
                    'grid': {
                        'color': "rgba(255, 255, 255, 0.3)",  # Light grid lines
                        'lineWidth': 0.5,
                    },
                },
            },
        }
    }
}

def connect_to_mysql(confs):
    try:
        conn = MySQLdb.Connection(
            host=confs.ip,
            user=confs.username,
            password=confs.password,
            port=int(confs.port),
            db=confs.schema
        )
    except :
        None

        
    return conn.cursor(MySQLdb.cursors.DictCursor)

    

def connect_to_oracle(confs):
    try:
        # https://stackoverflow.com/questions/10455863/making-a-dictionary-list-with-cx-oracle
        
        CONN_STR = '{username}/{password}@{ip}:{port}/{port}'.format(**confs)
        conn    = cx_Oracle.connect(CONN_STR)
        conn.ping()
    except :
        return None

    return conn.cursor()

    
def create_cursor(confs):

    if confs.connection_type == 'oracle':
        print('here')
        return connect_to_oracle(confs=confs)

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


    chart_type = chart.chart_type.name


    df              = pd.DataFrame(data)
    for col in y_cols:
        axis = ChartAxis.objects.filter(chart=chart, name=col).first()
        if axis and axis.axis == 'y':
            datasets.append({
                'yAxisID'               : 'y',
                'label'                 : axis.name,
                'borderColor'           : axis.color,
                'backgroundColor'       : axis.color,
                'data'                  : list(df[col]),
                'borderRadius'          : 50,
                'barThickness'          : 30,
                'tension'               : 0.4, 
                'fill'                  : True,
                'pointRadius'           : 5,
            })
    chart_data = {
        'data' : {
            'labels': list(df[x_cols]),
            'datasets': datasets
        },
        'options': charts_options[chart_type]['multiple' if len(y_cols) > 1 else 'single'],
        'utils' : {
            'type'  : chart_type,
            'width' : chart.width
        }
        
    }

    return chart_data


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



def check_db_connection(confs):
    
    cursor      = create_cursor(confs=confs)
    

    if not cursor:
        return False
    
    
        

    return False  