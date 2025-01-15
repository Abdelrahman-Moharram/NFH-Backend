import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import pdfkit

MODULES_NAMES = {
    'sessions':'sessions',
    'cases':'cases',
    'judgements':'judgements'
}


def paginate_query_set_list(query_set, params, ):
    page            = to_int(params.get('page'), 1)
    size            = to_int(params.get('size'), 10)
    
    
    count           = query_set.count()
    instances       = query_set[(page-1)*size : (page) * size]

    return {
        'instances'     : instances,
        'total_pages'   : int(count/size) or 1,
        'page'          : page,
        'size'          : size
    }


def get_file_full_path(path):
    if settings.DEBUG:
        return str(settings.BASE_DIR) +"\\media\\"+path.replace('/', '\\')
    else:
        return str(settings.BASE_DIR) +"/media/"+path


def export_as_excel(data, file_name, excluded_cols=[]):
    df = pd.DataFrame(data)
    
    if excluded_cols:
        df = df.drop(excluded_cols, axis=1)


    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.xlsx"'
    
    return response


def export_data_table_as_pdf(data, file_name, excluded_cols=[]):
    df = pd.DataFrame(data)

    if excluded_cols:
        df = df.drop(excluded_cols, axis=1)


    # Convert the DataFrame to a dictionary for template rendering
    columns = df.columns.tolist()

    template = get_template('pdf/datatable.html')

    html = template.render({'data': df.values, 'columns': columns})

    config = pdfkit.configuration(wkhtmltopdf=settings.PATH_WKHTMLTOPDF)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options ,  configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename=file_name
    return response






def to_int(val, default):
    if val:
        try:
            val = int(val)
            if val:
                return val
            return default
        except:
            pass
    return default