import plotly.express as px
import pandas as pd
import os
from pages_charts.charts_config import elegant_colors, colors_won_vs_lost, data
print("Current working directory:", os.getcwd())

fig_dist_won_lost = px.histogram(data, 
                  x='Stage',
                  title='Distribution of Won vs Lost Opportunities',
                  color='Stage',
                  text_auto=True,
                  color_discrete_sequence=["red", "blue"]
                  )  # Mostra os valores em cima das barras

fig_dist_won_lost.update_traces(textposition='outside')

if __name__ == "__main__":
    # This will execute when the script is run directly
    
    print(data.head())  # You can replace this with other code you need to execute
