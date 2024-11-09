from dash import Dash, dash_table, dcc, html, Input, Output, State, callback

import base64
import io
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Анализ данных о продажах и услуг'),
    html.Hr(),

    dcc.Upload(
        id='datatable-upload',
        children=html.Div([
            'Перетащите или ',
            html.A('Выберите Файлы')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        },
    ),

    html.Br(),
    html.H3('Таблица данных'),
#----------------------------------------- Таблица
    # dcc.DatePickerRange(
    #     id='date-picker-range-for-table',
    #     start_date = None,
    #     end_date = None,
    #     display_format='YYYY-MM-DD'
    # ),
    dash_table.DataTable(id='datatable-upload-container', page_size=10),
#----------------------------------------- Гистограмма
    # dcc.DatePickerRange(
    #     id='date-picker-range-for-hist',
    #     start_date = None,
    #     end_date = None,
    #     display_format='YYYY-MM-DD'
    # ),
    dcc.Graph(id='histogram'),
#----------------------------------------- Линейчатый график
    dcc.DatePickerRange(
        id='date-picker-range-for-line',
        start_date = None,
        end_date = None,
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='line'),
#----------------------------------------- График рассеяния
    dcc.DatePickerRange(
        id='date-picker-range-for-scat',
        start_date = None,
        end_date = None,
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='scat'),
#----------------------------------------- Круговая диаграмма
    dcc.Graph(id='pie'),
#----------------------------------------- Пузырьковая диаграмма
    dcc.Graph(id='bubble'),
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))
#------------------------------------------------------------------------------------- Таблица
#--------------------------------------------- Выбор даты для таблицы
# @callback(
#     Output('datatable-upload-container', 'table', allow_duplicate=True),
#     Input('date-picker-range-for-table', 'start_date'),
#     Input('date-picker-range-for-table', 'end_date'),
#     Input('datatable-upload', 'contents'),
#     State('datatable-upload', 'filename'),
#     prevent_initial_call=True
# )
#
# def update_graph(start_date, end_date, contents, filename):
#
#     data = parse_contents(contents, filename)
#     data['Дата'] = pd.to_datetime(data['Дата'])
#
#     if start_date == None or end_date == None:
#         return data.to_dict('records')
#
#     else:
#         filtered_data = data[(data['Дата'] >= start_date) & (data['Дата'] <= end_date)]
#         return filtered_data.to_dict('records')

#--------------------------------------------- Обратный вызов для таблицы V
@callback(Output('datatable-upload-container', 'data'),
              Output('datatable-upload-container', 'columns'),
              Input('datatable-upload', 'contents'),
              State('datatable-upload', 'filename'))
def update_output(contents, filename):
    if contents is None:
        return [{}], []
    df = parse_contents(contents, filename)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
#------------------------------------------------------------------------------------- Гистограмма V
#--------------------------------------------- Выбор даты для гистограммы
# @callback(
#     Output('histogram', 'figure', allow_duplicate=True),
#     Input('date-picker-range-for-hist', 'start_date'),
#     Input('date-picker-range-for-hist', 'end_date'),
#     Input('datatable-upload', 'contents'),
#     State('datatable-upload', 'filename'),
#     prevent_initial_call=True
# )
# def update_graph_hist(start_date, end_date, contents, filename):
#
#     data = parse_contents(contents, filename)
#     data['Дата'] = pd.to_datetime(data['Дата'])
#
#     if start_date == None or end_date == None:
#         figure = px.histogram(data, x=data['Дата'], y=data['Выручка'], title = 'Гистограмма анализа выручки за указанный период')
#         return figure
#
#     else:
#         filtered_data = data[(data['Дата'] >= start_date) & (data['Дата'] <= end_date)]
#         figure = px.histogram(data, x=filtered_data['Дата'], y=filtered_data['Выручка'], title = 'Гистограмма анализа выручки за указанный период')
#         return figure

#--------------------------------------------- Обратный вызов для гистограммы
@callback(Output('histogram', 'figure'),
              Input('datatable-upload-container', 'data'))
def display_hist(rows):
    df = pd.DataFrame(rows)

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return px.histogram(df, x='Категория', y='Выручка', histfunc='avg', title = 'Гистограмма анализа выручки за указанный период')

#------------------------------------------------------------------------------------- Линейчатый график V
#--------------------------------------------- Выбор даты для линейчатого графика
@callback(
    Output('line', 'figure', allow_duplicate=True),
    Input('date-picker-range-for-line', 'start_date'),
    Input('date-picker-range-for-line', 'end_date'),
    Input('datatable-upload', 'contents'),
    State('datatable-upload', 'filename'),
    prevent_initial_call=True
)
def update_graph_line(start_date, end_date, contents, filename):

    data = parse_contents(contents, filename)
    data['Дата'] = pd.to_datetime(data['Дата'])

    if start_date == None or end_date == None:
        figure = px.line(data, x=data['Дата'], y=data['Выручка'], title='Линейный график динамики доходов')
        return figure

    else:
        filtered_data = data[(data['Дата'] >= start_date) & (data['Дата'] <= end_date)]
        figure = px.line(data, x=filtered_data['Дата'], y=filtered_data['Выручка'], title='Линейный график динамики доходов')
        return figure
#--------------------------------------------- Обратный вызов для линейчатого графика
@callback(Output('line', 'figure'),
              Input('datatable-upload-container', 'data'))
def display_hist(rows):
    df = pd.DataFrame(rows)

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return px.line(df, x='Дата', y='Выручка', title = 'Линейный график динамики доходов')


#------------------------------------------------------------------------------------- График рассеяния V
#--------------------------------------------- Выбор даты для графика рассеяния
@callback(
    Output('scat', 'figure', allow_duplicate=True),
    Input('date-picker-range-for-scat', 'start_date'),
    Input('date-picker-range-for-scat', 'end_date'),
    Input('datatable-upload', 'contents'),
    State('datatable-upload', 'filename'),
    prevent_initial_call=True
)
def update_graph_line(start_date, end_date, contents, filename):

    data = parse_contents(contents, filename)
    data['Дата'] = pd.to_datetime(data['Дата'])

    if start_date == None or end_date == None:
        figure = px.scatter(data, x=data['Дата'], y=data['Выручка'], title='График рассеяния для анализа корреляции между количеством товара и приблью')
        return figure

    else:
        filtered_data = data[(data['Дата'] >= start_date) & (data['Дата'] <= end_date)]
        figure = px.scatter(data, x=filtered_data['Дата'], y=filtered_data['Выручка'], title='График рассеяния для анализа корреляции между количеством товара и приблью')
        return figure
#--------------------------------------------- Обратный вызов для графика рассеяния
@callback(Output('scat', 'figure'),
              Input('datatable-upload-container', 'data'))
def display_hist(rows):
    df = pd.DataFrame(rows)

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return px.scatter(df, x='Дата', y='Выручка', title = 'График рассеяния для анализа корреляции между количеством товара и приблью')

#------------------------------------------------------------------------------------- Круговая диаграмма V
@callback(Output('pie', 'figure'),
              Input('datatable-upload-container', 'data'))
def display_hist(rows):
    df = pd.DataFrame(rows)

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return px.pie(df, values = 'Выручка', names = 'Категория', title='Круговая диаграмма визуализации выручки по категориям')

#------------------------------------------------------------------------------------- Пузырьковая диаграмма V
@callback(Output('bubble', 'figure'),
              Input('datatable-upload-container', 'data'))
def display_hist(rows):
    df = pd.DataFrame(rows)

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return px.scatter(df, x="Количество", y="Выручка",
	         size="Сумма (в рублях)", color="Категория",
                 hover_name="Категория", log_x=True, size_max=60,title = 'Пузырьковая диаграмма')


if __name__ == '__main__':
    app.run(debug=True)
