from reports.models import ChartAxis, Chart
import pandas as pd

def data_to_chart_data(chart_id):
    x_cols = 'RECEIVABLES'
    y_cols = ['BUCKET_1', 'BUCKET_2', 'BUCKET_3', 'BUCKET_4', 'BUCKET_5', 'BUCKET_6']
    df = pd.read_csv('./96_data.csv')
    
    datasets    = []
    chart       = Chart.objects.filter(id=chart_id).first()
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