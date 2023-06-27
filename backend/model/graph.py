import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

def generateGraphs(data):
    finalScore = [60, 20, 40]
    categoryList = []
    categoryScoreList = []
    for i, apiCategory in enumerate(data):
        categoryList.append(apiCategory)
        categoryScoreList.append({})
        for key in data[apiCategory]:
            score = data[apiCategory][key]
            categoryScoreList[i][key] = score

    df = pd.DataFrame({'Category': categoryList,
                    'Scores': finalScore})
    
    colors = ['green' if score <= 50 else
            'yellow' if score <= 75 else
            'red' for score in df['Scores']]
    
    fig = go.Figure(data = go.Bar(x = df['Category'], y = df['Scores'], 
                customdata = categoryScoreList,
                marker = dict(color = colors)))
    
    hoverTemplate = 'Individual Scores:<br>%{customdata}<extra></extra>'
    customHoverData = []
    for category in fig.data[0].customdata:
        formattedData = []
        for key, value in category.items():
            print(fig.data[0].customdata)
            score_color = '🟢' if value <= 50 else '🟡' if value <= 75 else '🔴'
            formattedData.append(f"{score_color} <b>{key}</b>: {str(value)}")
        customHoverData.append(["<br>".join(formattedData)])

    fig.update_traces(hoverlabel = {'namelength': 0, 'bgcolor': 'white'}, 
                  hovertemplate = hoverTemplate,
                  customdata = customHoverData,
                  width = 0.5)
    
    fig.update_layout(title = 'Results Graph',
                    xaxis_title = 'Category',
                    yaxis_title = 'Score',
                    yaxis_range=[0, 100])
    
    pio.write_html(fig, file = './frontend/graph.html', full_html = False)



# aggregatedScores = {'GPTZero': 55, 
#                     'Writer': 65, 
#                     'Hugging Face': 75}
# hateSpeech = {'API 1': 70, 
#               'API 2': 80, 
#               'API 3': 90}
# misinformation = {'API A': 75, 
#                   'API B': 80, 
#                   'API C': 85}

generateGraphs({'ai gen':{'GPTZero': 55, 'Writer': 65, 'Hugging Face': 75}, 'hate speech':{'API 1': 70, 'API 2': 80, 'API 3': 90}, 'misinfo': {'API 1': 70, 'API 2': 80, 'API 3': 90}})







