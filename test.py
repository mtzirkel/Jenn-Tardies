import pandas as pd
import plotly.graph_objects as go
import pandas as pd

periods = ['Advisory', '1', '2', '3', '4', '5', '6', '7']
df = pd.read_csv('src/working_data.csv')
out_dict = {}
data = []
df = df[df['calendar_id'] == '21-22']
days = sorted(df['day_of_week'].unique().tolist(), reverse=True)

for day in days:
    trim_df = df[df['day_of_week'] == day]
    print(trim_df)
    period_lst = []
    for period in periods:
        if day == 'F' and period == 'Advisory':
            period_lst.append(0)
        else:
            trimmer_df = trim_df[trim_df['period'] == str(period)]
            daily_total = trimmer_df['tardies'].sum()
            period_lst.append(daily_total)

    out_dict[day] = period_lst
    data.append(
        go.Bar(name=day, x=periods, y=out_dict[day])
    )

fig = go.Figure(data=data)
fig.update_layout(barmode='group')
fig.show()
