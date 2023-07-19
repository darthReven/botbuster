import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd


def generate_gauge(data):
    category_list = []
    final_score = []
    for api_category in data:
        if api_category == 'sentence_data':
            continue
        category_list.append(api_category)
        if (not bool(data[api_category])):
            final_score.append(0)
        else:
            final_score.append(data[api_category]['average_score'])
    df = pd.DataFrame({'Category': category_list,
                    'Scores': final_score})
    representation = 70 / len(df)
    values = [0, 0, 0, 30] # R, O, G
    labels = ['Flagged', 'Potential Flag', 'Unflagged', ' ']
    hoverText = [[], [], [], []]

    for i, row in df.iterrows():
        score = row['Scores']
        category = row['Category']
        if score >= 80:
            values[0] += representation
            hoverText[0].append(f"🔴 <b>{category}</b>: {score}")
        elif score >= 20:
            values[1] += representation
            hoverText[1].append(f"🟠 <b>{category}</b>: {score}")
        else:
            values[2] += representation
            hoverText[2].append(f"🟢 <b>{category}</b>: {score}")

    hoverTextFormatted = []
    for category in hoverText:
        if len(category) != 0:
            hoverTextFormatted.append("Category(s):<br>" + "<br>".join(category) + "<extra></extra>")
        else:
            hoverTextFormatted.append(None)

    fig = go.Figure(data = [go.Pie(
        values = values,
        labels = labels,
        customdata = hoverTextFormatted,
        hole = 0.65,
        rotation = -126,
        sort = False,
        direction = "clockwise",
        textinfo = "none",
        hovertemplate = '%{customdata}',
        showlegend = True
    )])

    fig.add_annotation(
        text = "<b>Flagged:</b> {}<br><b>Potential Flag:</b> {}<br><b>Unflagged:</b> {}".format(
            len(df[df['Scores'] >= 80]),
            len(df[(df['Scores'] >= 20) & (df['Scores'] < 80)]),
            len(df[df['Scores'] < 20])
        ),
        x = 0.5,
        y = 0.5,
        font = dict(size=8),
        showarrow = False
    )

    fig.update_traces(marker = dict(colors=['#D2411A', '#E5801A', '#A3D23C', 'white'],
                    line = dict(color = 'white', width = 5)),
                    hoverlabel = {'bgcolor': 'white'})

    fig.update_layout(
        legend = dict(
            orientation = "h",
            x = 0.52,
            y = 0.13,
            xanchor = 'center',
            yanchor = 'top'
        ),
        margin = dict(
            l=0, r=0, t=0, b=0
        )
    )

    pio.write_html(fig, file = "../frontend/public/gauge.html", full_html = False)