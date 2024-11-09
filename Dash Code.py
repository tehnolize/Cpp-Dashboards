from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

df = pd.read_excel(r'E:\Users\Тариэль\Desktop\Вузовская шняга\СПС 2\Построение дашбордов\ЛБ\О продажах товаров или услуг.xlsx')

app = Dash()

app.layout = [
    html.H1('Анализ данных о продажах и услуг'),
    html.Hr(),

    html.H3('Таблица данных'),
    dash_table.DataTable(data =df.to_dict('records'), page_size=10),

    dcc.Graph(figure=px.histogram(df, x='Категория', y='Выручка', histfunc='avg', title = 'Гистограмма анализа прибыли и ее распределения')),

    dcc.Graph(figure=px.line(df, x='Дата', y='Выручка', title='Линейный график динамики доходов')),

    dcc.Graph(figure=px.scatter(df, x='Количество', y='Выручка', title='График рассеяния для анализа корреляции между количеством товара и приблью')),

    dcc.Graph(figure=px.pie(df, values='Выручка', names='Категория', title='Круговая диаграмма визуализации выручки по категориям')),

    dcc.Graph(figure=px.scatter(df, x="Количество", y="Выручка",
	         size="Сумма (в рублях)", color="Категория",
                 hover_name="Категория", log_x=True, size_max=60,title = 'Пузырчатая диаграмма'))
]

if __name__ == '__main__':
    app.run(debug=True)