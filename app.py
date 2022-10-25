from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib

app = Dash(__name__)
server = app.server


def get_pandas_data(csv_filename: str) -> pd.DataFrame:
    '''
    Load data from /data directory as a pandas DataFrame
    using relative paths. Relative paths are necessary for
    data loading to work in Heroku.
    '''
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(csv_filename))


df = get_pandas_data("working_data.csv")

year_legend = {0: '15-16', 1: '16-17', 2: '17-18', 3: '18-19',
               4: '19-20', 5: '20-21', 6: '21-22'}
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            ['total_absences', 'excused', 'unexcused', 'tardies'],
            'unexcused',
            id='attendance-type'
        ),
        dcc.RadioItems(['By Day ON', 'By Day OFF'], 'By Day ON', inline=True, id='by-day')
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div(id='total-students', style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    dcc.Graph(id='output'),
    dcc.Slider(0, 6,
               step=1,
               marks=year_legend,
               value=6,
               id='year-slider')
])


@app.callback(
    Output('output', 'figure'),
    Input('year-slider', 'value'),
    Input('attendance-type', 'value'),
    Input('by-day', 'value'))
def update_graph(year, attendance_type, by_day):
    periods = ['Advisory', '1', '2', '3', '4', '5', '6', '7']
    trim_df = df[df['calendar_id'] == year_legend[year]]
    period_abs = {}
    if by_day == 'By Day OFF':
        for period in periods:
            df_period = trim_df[trim_df['period'] == period]
            att_count = df_period[attendance_type].sum()
            # if period == 'Advisory':
            #     period = 0
            period_abs[period] = att_count
        df_output = pd.DataFrame({
            'Period': period_abs.keys(),
            f'Total {attendance_type}': period_abs.values()
        })

        fig = px.bar(df_output, x='Period', y=f'Total {attendance_type}')
    else:
        days = sorted(trim_df['day_of_week'].unique().tolist(), reverse=True)
        data = []
        for day in days:
            trimed_df = trim_df[trim_df['day_of_week'] == day]

            period_lst = []
            for period in periods:
                if day == 'F' and period == 'Advisory':
                    period_lst.append(0)
                else:
                    trimmer_df = trimed_df[trimed_df['period'] == str(period)]
                    daily_total = trimmer_df['tardies'].sum()
                    period_lst.append(daily_total)

            period_abs[day] = period_lst
            data.append(
                go.Bar(name=day, x=periods, y=period_abs[day])
            )

        fig = go.Figure(data=data)
        fig.update_layout(barmode='group')
    return fig


@app.callback(
    Output('total-students', 'children'),
    Input('year-slider', 'value'))
def update_totals(year):
    df_trim = df[df['calendar_id'] == year_legend[year]]
    students = len(df_trim['lunch#'].unique())
    return html.H3(f'{students} Students(all year)')


if __name__ == '__main__':
    app.run_server(debug=True)
