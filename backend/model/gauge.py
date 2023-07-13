import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

df = pd.DataFrame({'Category': ['AI-Generated Content', 'Hate Speech', 'Misinformation'],
                   'Scores': [80, 90, 30]})

representation = 70 / len(df)
values = [0, 0, 0, 30] # R, O, G
labels = ['Flagged', 'Potential Flag', 'Unflagged', ' ']
hoverText = [[], [], [], []]

for i, row in df.iterrows():
    score = row['Scores']
    category = row['Category']
    if score >= 75:
        values[0] += representation
        hoverText[0].append(f"🔴 <b>{category}</b>: {score}")
    elif score >= 50:
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
        len(df[df['Scores'] >= 75]),
        len(df[(df['Scores'] >= 50) & (df['Scores'] < 75)]),
        len(df[df['Scores'] < 50])
    ),
    x = 0.5,
    y = 0.5,
    font = dict(size=12),
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
    )
)

pio.write_html(fig, file = "../../frontend/public/gauge.html", full_html = False)