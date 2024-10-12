import plotly.graph_objects as go
import numpy as np
from query import get_user_averages

def create_scatter_plot(x, y, title, x_title, y_title, text):
    fig = go.Figure(data=go.Scatter(
        x=x,
        y=y,
        mode='markers',
        text=text,
        hovertemplate=f'User: %{{text}}<br>{x_title}: %{{x:.2f}}<br>{y_title}: %{{y:.2f}}',
        marker=dict(size=10, color='rgba(0, 128, 0, 0.8)')
    ))

    if len(x) > 1:
        z = np.polyfit(x, y, 2)
        p = np.poly1d(z)
        trend_x = np.linspace(min(x), max(x), 100)
        trend_y = p(trend_x)
        fig.add_trace(go.Scatter(
            x=trend_x,
            y=trend_y,
            mode='lines',
            line=dict(color='purple', width=2),
            name='Trend Line'
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        hovermode='closest',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        title_font=dict(color='white'),
        xaxis=dict(gridcolor='gray'),
        yaxis=dict(gridcolor='gray'),
        autosize=True,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )

    fig.update_layout(dragmode=False)
    
    config = {'displayModeBar': False, 'staticPlot': False}
    
    return fig, config

def get_column_data(data, column_names, column):
    index = column_names.index(column)
    return [row[index] for row in data if row[index] is not None]

def steps_distance_scatterplot():
    column_names, data = get_user_averages()
    
    avg_steps = get_column_data(data, column_names, 'avg_steps')
    avg_distance = get_column_data(data, column_names, 'avg_distance')
    user_ids = get_column_data(data, column_names, 'user_id')
    
    fig, config = create_scatter_plot(
        x=avg_steps,
        y=avg_distance,
        title='Average Steps vs Average Distance by User',
        x_title='Average Steps',
        y_title='Average Distance (km)',
        text=user_ids
    )
    return fig, config

def calorie_active_scatterplot():
    column_names, data = get_user_averages()
    
    avg_steps = get_column_data(data, column_names, 'avg_steps')
    avg_calories = get_column_data(data, column_names, 'avg_calories')
    user_ids = get_column_data(data, column_names, 'user_id')
    
    filtered_data = [(s, c, u) for s, c, u in zip(avg_steps, avg_calories, user_ids) if c >= 300]
    filtered_steps, filtered_calories, filtered_ids = zip(*filtered_data) if filtered_data else ([], [], [])
    
    fig = create_scatter_plot(
        x=filtered_steps,
        y=filtered_calories,
        title='Average Steps vs Average Calories by User',
        x_title='Average Steps',
        y_title='Average Calories',
        text=filtered_ids
    )
    
    return fig

def heart_sleep_scatterplot():
    column_names, data = get_user_averages()
    
    avg_minutes_asleep = get_column_data(data, column_names, 'avg_minutes_asleep')
    avg_heart_rate = get_column_data(data, column_names, 'avg_heart_rate')
    user_ids = get_column_data(data, column_names, 'user_id')

    filtered_data = [(s, h, u) for s, h, u in zip(avg_minutes_asleep, avg_heart_rate, user_ids) 
                     if s is not None and h is not None and s >= 300]
    filtered_sleep, filtered_heart_rate, filtered_ids = zip(*filtered_data) if filtered_data else ([], [], [])
    
    fig = create_scatter_plot(
        x=filtered_sleep,
        y=filtered_heart_rate,
        title='Average Sleep vs Average Heart Rate by User',
        x_title='Average Sleep (minutes)',
        y_title='Average Heart Rate (bpm)',
        text=filtered_ids
    )
    
    return fig