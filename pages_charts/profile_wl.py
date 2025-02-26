import plotly.express as px
import pandas as pd
from pages_charts.charts_config import elegant_colors, colors_won_vs_lost, data

# ======= Won vs. Lost Profile Analysis Charts ============

### -----------  Account Type --------------
fig_wl_acc_type_count = px.histogram(data, 
                  x=' Account Type',
                  color='Stage',
                  title='Distribution of Won vs Lost Opportunities by Account Type',
                  barmode='group',    # Para agrupar as barras lado a lado
                  text_auto=True,
                  color_discrete_sequence=colors_won_vs_lost
                  )     # Mostra os valores em cima das barras

fig_wl_acc_type_count.update_traces(textposition='outside')
fig_wl_acc_type_count.update_layout(
    width=1200,
    height=700,
    xaxis_title="Account Type",
    yaxis_title="Count",
    legend_title="Stage"
)

fig_wl_acc_type_pct = px.histogram(data, 
                  x=' Account Type',
                  color='Stage',
                  title='Distribution of Won vs Lost Opportunities by Account Type',
                  barmode='group',    # Para agrupar as barras lado a lado
                  text_auto=True,
                  color_discrete_sequence=colors_won_vs_lost
                  )     # Mostra os valores em cima das barras

fig_wl_acc_type_pct.update_traces(textposition='outside')
fig_wl_acc_type_pct.update_layout(
    width=1200,
    height=700,
    xaxis_title="Account Type (%)",
    yaxis_title="Count",
    legend_title="Stage"
)


### -----------  Country --------------

fig_wl_country = px.histogram(data, 
                  x='Country',
                  color='Stage',
                  title='Distribution of Won vs Lost Opportunities by Country',
                  barmode='group',    # Para agrupar as barras lado a lado
                  text_auto=True,
                  color_discrete_sequence=colors_won_vs_lost
                  )     # Mostra os valores em cima das barras

fig_wl_country.update_traces(textposition='outside')
fig_wl_country.update_layout(
    width=1200,
    height=700,
    xaxis_title="Country",
    yaxis_title="Count",
    legend_title="Stage"
)

# Count occurrences of each stage per country
data_grouped = data.groupby(['Country', 'Stage']).size().reset_index(name='count')

# Calculate proportions
data_grouped['percentage'] = data_grouped.groupby('Country')['count'].transform(lambda x: x / x.sum() * 100)

# Create stacked bar chart for proportions
fig_wl_country_pct = px.bar(data_grouped, 
             x='Country', 
             y='percentage', 
             color='Stage', 
             title='Proportion of Won vs Lost Opportunities by Country',
             text_auto='.2f',  # Show percentage labels
             color_discrete_sequence=colors_won_vs_lost,
             barmode='stack')  # Stack bars to represent proportions

# Update layout for better readability
fig_wl_country_pct.update_layout(
    width=1200,
    height=700,
    xaxis_title="Country",
    yaxis_title="Percentage (%)",
    legend_title="Stage",
    yaxis=dict(tickformat=".1f")  # Format y-axis as percentage
)

### -----------  Segment --------------


# Define the correct order of Segments and Stages
segment_order = ["Segment 1", "Segment 2", "Segment 3", "Segment 4", "Unknow"]
stage_order = ["Closed Lost", "Closed Won"]  # Ensure Lost is before Won

# Histogram for absolute count
fig_wl_segment = px.histogram(data, 
                  x='Stage',
                  color='Segment',
                  title='Distribution of Won vs Lost Opportunities by Segment',
                  barmode='group',    
                  color_discrete_sequence=elegant_colors,
                  text_auto=True,
                  category_orders={"Segment": segment_order, "Stage": stage_order}  # Enforce segment and stage order
                  )     

fig_wl_segment.update_traces(textposition='outside')
fig_wl_segment.update_layout(
    width=1200,
    height=700,
    xaxis_title="Stage",
    yaxis_title="Count",
    legend_title="Segment"
)

# -------------------- #
# Calculate the percentage of each segment within each stage
data_percentage = data.groupby(['Stage', 'Segment']).size().reset_index(name='count')

# Normalize to percentage
data_percentage['percentage'] = data_percentage.groupby('Stage')['count'].transform(lambda x: x / x.sum() * 100)

# Histogram for proportion (percentage)
fig_wl_segment_pct = px.bar(data_percentage, 
             x='Stage', 
             y='percentage', 
             color='Segment', 
             title='Proportion of Won vs Lost Opportunities by Segment',
             text_auto='.2f',  
             barmode='stack',  
             color_discrete_sequence=elegant_colors,  
             category_orders={"Segment": segment_order, "Stage": stage_order}  # Enforce segment and stage order
             )

fig_wl_segment_pct.update_traces(textposition='inside')
fig_wl_segment_pct.update_layout(
    width=1200,
    height=700,
    xaxis_title="Stage",
    yaxis_title="Percentage",
    legend_title="Segment",
    yaxis=dict(tickformat=".1f%")  
)


### -----------  Time Analysis --------------

# Filter data to include only closed deals (Closed Won and Closed Lost)
closed_data = data[data["Stage"].isin(["Closed Won", "Closed Lost"])].copy()

# ---------------------------
# Monthly Aggregation
# ---------------------------
# Aggregate by month and stage (counts)
monthly = closed_data.groupby([pd.Grouper(key='Close Date', freq='M'), 'Stage']).size().reset_index(name='Count')
# Calculate percentage per month
monthly['Percentage'] = monthly.groupby('Close Date')['Count'].transform(lambda x: x / x.sum() * 100)

# Create monthly count plot (stacked bar)
fig_wl_month = px.bar(
    monthly, 
    x='Close Date', 
    y='Count', 
    color='Stage',
    title="Monthly Proportional Comparison of WON vs. LOST Deals (Counts)",
    labels={'Close Date': 'Month', 'Count': 'Number of Deals'},
    barmode='stack',
    color_discrete_sequence=["red", "blue"],
    text_auto=True
)
fig_wl_month.update_layout(width=1200, height=600)

# Create monthly percentage plot (stacked bar)
fig_wl_month_pct = px.bar(
    monthly, 
    x='Close Date', 
    y='Percentage', 
    color='Stage',
    title="Monthly Proportional Comparison of WON vs. LOST Deals (Percentage)",
    labels={'Close Date': 'Month', 'Percentage': 'Percentage (%)'},
    barmode='stack',
    color_discrete_sequence=["red", "blue"],
    text_auto='.1f'
)
fig_wl_month_pct.update_layout(width=1200, height=600)

# ---------------------------
# Quarterly Aggregation
# ---------------------------
# Aggregate by quarter and stage (counts)
quarterly = closed_data.groupby([pd.Grouper(key='Close Date', freq='Q'), 'Stage']).size().reset_index(name='Count')
# Calculate percentage per quarter
quarterly['Percentage'] = quarterly.groupby('Close Date')['Count'].transform(lambda x: x / x.sum() * 100)

# Create quarterly count plot (stacked bar)
fig_wl_quarter = px.bar(
    quarterly, 
    x='Close Date', 
    y='Count', 
    color='Stage',
    title="Quarterly Proportional Comparison of WON vs. LOST Deals (Counts)",
    labels={'Close Date': 'Quarter', 'Count': 'Number of Deals'},
    barmode='stack',
    color_discrete_sequence=["red", "blue"],
    text_auto=True
)
fig_wl_quarter.update_layout(width=1200, height=600)

# Create quarterly percentage plot (stacked bar)
fig_wl_quarter_pct = px.bar(
    quarterly, 
    x='Close Date', 
    y='Percentage', 
    color='Stage',
    title="Quarterly Proportional Comparison of WON vs. LOST Deals (Percentage)",
    labels={'Close Date': 'Quarter', 'Percentage': 'Percentage (%)'},
    barmode='stack',
    color_discrete_sequence=["red", "blue"],
    text_auto='.1f'
)
fig_wl_quarter_pct.update_layout(width=1200, height=600)

if __name__ == "__main__":
    # This will execute when the script is run directly
    print(data.head())  # You can replace this with other code you need to execute
