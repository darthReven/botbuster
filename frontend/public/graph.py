import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

df = pd.DataFrame({'Category': ['Aggregated Score', 'Hate Speech', 'Misinformation'],
                   'Scores': [60, 75, 80]})

aggregatedScores = {'GPTZero': 55, 
                    'Writer': 65, 
                    'Hugging Face': 75}
hateSpeech = {'API 1': 70, 
              'API 2': 80, 
              'API 3': 90}
misinformation = {'API A': 75, 
                  'API B': 80, 
                  'API C': 85}

colors = ['green' if score <= 50 else
          'yellow' if score <= 75 else
          'red' for score in df['Scores']]

threshold = 50

fig = go.Figure()

# Bar Graph
fig.add_trace(go.Bar(x = df['Category'], y = df['Scores'], 
                             customdata = [aggregatedScores, hateSpeech, misinformation],
                             marker = dict(color = colors),
                             width = 0.4))

# Threshold Indicator
# all the way
fig.add_shape(
    type = 'line',
    x0 = -0.5,
    y0 = threshold,
    x1 = len(df['Category']) - 0.5,
    y1 = threshold,
    line = dict(color = 'silver', dash ='dash'),
    name = f'Threshold ({threshold})'
)
# not all the way
'''fig.add_trace(go.Scatter( x= [df['Category'][0], df['Category'].iloc[-1]],
    y = [threshold, threshold],
    mode = 'lines',
    line = dict(color='silver', dash = 'dash')))'''

hoverTemplate = 'Individual Scores:<br>%{customdata}<extra></extra>'
customHoverData = []
for category in fig.data[0].customdata:
    formattedData = []
    for key, value in category.items():
        score_color = '🟢' if value <= 50 else '🟠' if value <= 75 else '🔴'
        formattedData.append(f"{score_color} <b>{key}</b>: {str(value)}")
    customHoverData.append(["<br>".join(formattedData)])
    
fig.update_traces(hoverlabel = {'namelength': 0, 'bgcolor': 'white'}, 
                  hovertemplate = hoverTemplate,
                  customdata = customHoverData)

fig.update_layout(title = 'Results Graph',
                  xaxis_title = 'Category',
                  yaxis_title = 'Score',
                  yaxis_range=[0, 100],
                  barmode = 'group',
                  showlegend = False,
                  margin = dict(l=0, r=0, t=0, b=0))

pio.write_html(fig, file = 'gauge-graph.html', full_html = False)