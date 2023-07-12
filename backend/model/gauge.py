import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

df = pd.DataFrame({'Category': ['AI-Generated Content', 'Hate Speech', 'Misinformation'],
                   'Scores': [80, 90, 30]})

representation = 100 / len(df)
values = [0, 0, 0] # R, O, G
labels = ['Flagged', 'Potential Flag', 'Unflagged']
hoverText = [[], [], []]

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
    hoverTextFormatted.append("<br>".join(category))

fig = go.Figure(data = [go.Pie(
    values = values,
    labels = labels,
    customdata = hoverTextFormatted,
    hole = 0.65,
    rotation = -126,
    sort = False,
    direction = "clockwise",
    textinfo = "none",
    hovertemplate = 'Category(s):<br>%{customdata}<extra></extra>',
    showlegend = True
)])

fig.update_traces(marker = dict(colors=['#D2411A', '#E5801A', '#A3D23C', 'white'],
                  line = dict(color = 'white', width = 5)),
                  hoverlabel = {'bgcolor': 'white'})

fig.update_layout(
    legend = dict(
        orientation = "h",
        x = 0.5,
        y = -0.05,
        xanchor = 'center',
        yanchor = 'top'
    )
)

pio.write_html(fig, file = "../../frontend/public/gauge.html", full_html = False)