import pandas as pd

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set custom layout for plotly
pio.templates['custom'] = go.layout.Template(
    layout= dict(
        font=dict(family='Courier New', size=15),
        title=dict(
            font=dict(family='Courier New', size=25),
            x=0.5
        ),
        bargap=0.1,
        width=1000,
        height=800,
        autosize=False
    )
)
pio.templates.default = 'plotly+custom'


def get_hist_by_sex_work_days(df: pd.DataFrame, work_days: int) -> go.Figure:
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=['Распределение возраста (мужчины)',
                        'Распределение возраста (женщины)'],
        vertical_spacing=0.1
    )

    fig.add_trace(
        go.Histogram(
            x=df.loc[df['Пол'] == 'М', 'Возраст'],
            name='Все значения'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Histogram(
            x=df.loc[(df['Пол'] == 'М') & (df['Количество больничных дней'] > work_days), 'Возраст'],
            name=f'Больничных дней > {work_days}'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Histogram(
            x=df.loc[df['Пол'] == 'Ж', 'Возраст'],
            name='Все значения'
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Histogram(
            x=df.loc[(df['Пол'] == 'Ж') & (df['Количество больничных дней'] > work_days), 'Возраст'],
            name=f'Больничных дней > {work_days}'
        ),
        row=2, col=1
    )

    fig.update_layout(
        title_text='Распределение возраста',
        yaxis1_title='Количество значений',
        yaxis2_title='Количество значений',
        xaxis2_title='Возраст',
    )

    return fig


def get_whisker_plot_by_sex_work_days(
        df: pd.DataFrame, work_days: int) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Box(
            x=df.query('`Пол` == "М"')['Возраст'],
            boxmean=True,
            name='М (все значения)',
            showlegend=False
        ),
    )

    fig.add_trace(
        go.Box(
            x=df.query(f'`Пол` == "М" and `Количество больничных дней` > {work_days}')['Возраст'],
            boxmean=True,
            name=f'М (кол-во больничных дней > {work_days})',
            showlegend=False
        ),
    )

    fig.add_trace(
        go.Box(
            x=df.query('`Пол` == "Ж"')['Возраст'],
            boxmean=True,
            name='Ж (все значения)',
            showlegend=False
        ),
    )

    fig.add_trace(
        go.Box(
            x=df.query(f'`Пол` == "Ж" and `Количество больничных дней` > {work_days}')['Возраст'],
            boxmean=True,
            name=f'Ж (кол-во больничных дней > {work_days})',
            showlegend=False
        ),
    )

    fig.update_layout(
        title_text='Диаграмма размаха возраста (по полу) *пунктиром - среднее значение',
        yaxis_title='Пол',
        xaxis_title='Возраст',
    )

    return fig


def get_hist_by_age_work_days(
        df: pd.DataFrame, work_days: int, age: int) -> go.Figure:

    df['older_than_age'] = (
        df['Возраст']
        .apply(lambda x: 'Да' if x > age else 'Нет')
    )
    df['more_than_work_days'] = (
        df['Количество больничных дней']
        .apply(lambda x: 'Да' if x > work_days else 'Нет')
    )

    fig = px.histogram(
        df,
        x='Возраст',
        color='older_than_age',
        pattern_shape='more_than_work_days'
    )

    fig.update_layout(
        title_text='Распределение возраста',
        legend_title_text=f'Старше {age} лет,'
                          + f'<br>Больничных дней > {work_days}',
        yaxis_title='Количество значений',
    )

    return fig


def get_hist_by_age_work_days_small(
        df: pd.DataFrame, work_days: int) -> go.Figure:

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df['Возраст'],
            name='Все значения'
        )
    )

    fig.add_trace(
        go.Histogram(
            x=df.query(f'`Количество больничных дней` > {work_days}')['Возраст'],
            name=f'Больничных дней > {work_days}'
        )
    )

    fig.update_layout(
        title_text='Распределение возраста',
        yaxis_title='Количество значений',
    )

    return fig
