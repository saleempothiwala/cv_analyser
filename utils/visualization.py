# utils/visualization.py
import plotly.graph_objects as go
import tempfile
import os

def create_radar_chart(analysis_dict):
    """Create a radar chart from analysis scores"""
    categories = list(analysis_dict.keys())
    values = list(analysis_dict.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values + values[:1],  # Close the polygon
        theta=categories + categories[:1],
        fill='toself',
        fillcolor='rgba(255,107,53,0.5)',
        line=dict(color='#292929')
    )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(color='#292929')
            )
        ),
        paper_bgcolor='white',
        width=500,
        height=400
    )
    
    # Save to temp file for PDF reporting
    temp_dir = tempfile.mkdtemp()
    chart_path = os.path.join(temp_dir, 'radar_chart.png')
    fig.write_image(chart_path)
    
    return chart_path