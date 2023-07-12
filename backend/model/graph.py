import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

def generate_graph(data):
    final_score = []
    category_list = []
    category_score_list = []
    for i, api_category in enumerate(data):
        category_list.append(api_category)
        category_score_list.append({})
        if (not bool(data[api_category])):
            final_score.append(0)
        for key in data[api_category]:
            if key != "overall_score":
                score = data[api_category][key]
                category_score_list[i][key] = score
            else:
                final_score.append(data[api_category][key])
    df = pd.DataFrame({'Category': category_list,
                    'Scores': final_score})
    
    # scores are current hard coded
    colors = ['green' if score <= 50 else
            'yellow' if score <= 75 else
            'red' for score in df['Scores']]
    
    fig = go.Figure(data = go.Bar(x = df['Category'], y = df['Scores'], 
                customdata = category_score_list,
                marker = dict(color = colors)))
    
    hover_template = 'Individual Scores:<br>%{customdata}<extra></extra>'
    custom_hover_data = []
    for category in fig.data[0].customdata:
        formatted_data = []
        for key, value in category.items():
            if type(value) is int or type(value) is float:
                score_color = '🟢' if value <= 50 else '🟡' if value <= 75 else '🔴'
                formatted_data.append(f"{score_color} <b>{key}</b>: {str(value)}")
            else:
                formatted_data.append(f"⚪<br>{key}</b>: {str(value)}")
        custom_hover_data.append(["<br>".join(formatted_data)])

    fig.update_traces(hoverlabel = {'namelength': 0, 'bgcolor': 'white'}, 
                  hovertemplate = hover_template,
                  customdata = custom_hover_data,
                  width = 0.5)
    
    fig.update_layout(title = 'Results Graph',
                    xaxis_title = 'Category',
                    yaxis_title = 'Score',
                    yaxis_range=[0, 100])
    
    pio.write_html(fig, file = '../../frontend/public/graph.html', full_html = False)



# aggregatedScores = {'GPTZero': 55, 
#                     'Writer': 65, 
#                     'Hugging Face': 75}
# hateSpeech = {'API 1': 70, 
#               'API 2': 80, 
#               'API 3': 90}
# misinformation = {'API A': 75, 
#                   'API B': 80, 
#                   'API C': 85}






