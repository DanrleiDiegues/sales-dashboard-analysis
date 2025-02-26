import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import os
from pages_charts.profile_wl import fig_wl_acc_type_count, fig_wl_acc_type_pct, fig_wl_country, fig_wl_country_pct

st.set_page_config(
    page_title="Sales Opportunities Dashboard (2024)",
    page_icon="📊", # 📈 
    layout="wide",
    initial_sidebar_state="expanded"
    )

# Obter o caminho base do diretório onde o app.py está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------- Load the Charts -----------

@st.cache_data  # Caches the function's output to optimize performance in Streamlit.
def load_graphics():
    graphics = {}  # Dictionary to store the loaded graphics.
    file_paths = [
        "charts/fig_dist_won_lost.pkl",
        "charts/fig_wl_acc_type_count.pkl",
        "charts/fig_wl_acc_type_pct.pkl",
        "charts/fig_wl_country.pkl",
        "charts/fig_wl_country_pct.pkl",
        "charts/fig_wl_segment.pkl",
        "charts/fig_wl_segment_pct.pkl",
        "charts/fig_wl_month.pkl", 
        "charts/fig_wl_month_pct.pkl",
        "charts/fig_wl_quarter.pkl",
        "charts/fig_wl_quarter_pct.pkl",
        "charts/fig_month_value.pkl",
        "charts/fig_month_value_pct.pkl",
        "charts/fig_quarter_value.pkl",
        "charts/fig_quarter_value_pct.pkl",

        "charts/fig_wl_lead_source.pkl",
        "charts/fig_wl_lead_source_pct.pkl",
        "charts/fig_wl_type_business_count.pkl",
        "charts/fig_wl_type_business_pct.pkl",
        "charts/fig_won_wl_acc_type_pct.pkl",
        "charts/fig_lost_wl_acc_type_pct.pkl",
        "charts/fig_wl_close_reason_count.pkl",
        "charts/fig_wl_close_reason_pct.pkl",
        "charts/fig_quarter_value_pct.pkl",
        
        "charts/fig_wl_avg_ticket.pkl",
        "charts/fig_wl_avg_ticket_account_type.pkl",
        "charts/fig_wl_avg_ticket_country.pkl",
        "charts/fig_wl_avg_ticket_segment.pkl",
        
        "charts/fig_wl_avg_time.pkl",
        "charts/fig_wl_avg_time_account_type.pkl",
        "charts/fig_wl_avg_time_type_business.pkl",
        
    ]

    for path in file_paths:
        full_path = os.path.join(BASE_DIR, path)  # Creates the absolute path to the file.
        try:
            if os.path.exists(full_path):  # Checks if the file exists.
                with open(full_path, "rb") as file:  # Opens the file in read-binary mode.
                    filename = os.path.basename(path)  # Extracts the filename.
                    graphics[filename] = pickle.load(file)  # Loads the figure into the dictionary.
            else:
                st.warning(f"File {path} not found.")  # Displays a warning in Streamlit if the file is missing.
        except Exception as e:
            st.error(f"Error loading {path}: {e}")  # Displays an error message if loading fails.

    return graphics  # Returns the dictionary containing the loaded graphics.

graphics = load_graphics()  # Calls the function and stores the results in the `graphics` variable.

# ------------- Load the Data ----------

data = pd.read_csv("data/sales_preprocessed_data.csv")


# ------ Merck Logo -------

logo_path = os.path.join(BASE_DIR, "docs/merck_logo_blue.png")

if os.path.exists(logo_path):
    st.image(logo_path, width=200)
else:
    st.error(f"Logo não encontrado: {logo_path}")


# --------- APP -----------

st.sidebar.title("Navegação")
page = st.sidebar.selectbox("Escolha uma página", 
                            ["Home | Overview",
                             "Profile | WON vs. LOST",
                             "Average Ticket Analysis",
                             "Average Time to Close",
                             "Prediction",
                             "Agent Assistant"
                             ]
    )


# ----------- HOME PAGE --------------
if page == "Home | Overview":
    
    st.title("Home")
    st.header('Overview data')
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_dist_won_lost.pkl"], use_container_width=True)
    with col2:
        st.plotly_chart(graphics["fig_dist_won_lost.pkl"], use_container_width=True)
    
    # Add notes:
    st.markdown("""
    **Notes:**
    - As we can see, we have a balanced dataset between Won and Lost Opportunities to Analyse.
    """)
    
    st.subheader("Dataset Details")
    
    st.dataframe(data)

    st.text_area("Comment about the charts:", "Add your observations..")
        
        
# ----------- PROFILE PAGE --------------
elif page == "Profile | WON vs. LOST":
    
    st.title("Profiles")
    st.header('Profile between WON vs. LOST')
    st.markdown("""
    **Questions to address**:
    - What are the main reasons for winning/lossing an opportunity?
    - What is the profile of the won opportunities?
    - What is the profile of the lost opportunities?
    - What are the main differences between the two profiles?
    - Which factors appear most frequently?
            """)
    
    
    # ======= Won vs. Lost Profile Analysis Charts ============
    
    
    ### -----------  Close Reasons --------------
    st.subheader('Close Reason Analysis')
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_close_reason_count.pkl"], use_container_width=True)
        
    with col2:
        st.plotly_chart(graphics["fig_wl_close_reason_pct.pkl"], use_container_width=True)
        
    st.markdown("""
    Notes | Close Reason:
    "Automatically" was main for both. However, doesn't considerin it, we have:

    - The Top 3 Closed Lost reasons: Project/Budget Cancelled/Out of Business (6.92%), Price (5.97%), Unable to confirm Sale (3.56%)
    - The Top 3 Closed Won reasons: Brand Recognition/Supplier Reputation (13.01%), Customer Relationship (11.22%), Price (9.19%)
    - Insight: These patterns suggest that strong brand recognition and supplier reputation are key drivers for success, while price plays a significant role in both won and lost opportunities. 
    The higher impact of customer relationships on closed-won deals highlights the importance of maintaining strong connections with clients.
    """)
   
    

    ### -----------  Account Type --------------
    st.subheader('Account Type')
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_acc_type_count.pkl"], use_container_width=True)
        
    with col2:
        st.plotly_chart(graphics["fig_wl_acc_type_pct.pkl"], use_container_width=True)
        
    st.markdown("""
    Notes | Account Type:
    - Small Accounts account for the highest proportion of LOST deals, with 51.89% LOST compared to 48.11% WON.
    - Top 1 Accounts, on the other hand, have a lower loss rate, with only 38.98% resulting in a loss and 61.02% being successfully closed.
    - This suggests that larger accounts have a higher chance of success, while small accounts face more challenges in closing deals.
    """)
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_won_wl_acc_type_pct.pkl"], use_container_width=True)
    with col2:
        st.plotly_chart(graphics["fig_lost_wl_acc_type_pct.pkl"], use_container_width=True)
    
    
    
    ### -----------  Country --------------
    st.subheader('Country')
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_country.pkl"], use_container_width=True)
    with col2:
        st.plotly_chart(graphics["fig_wl_country_pct.pkl"], use_container_width=True)
    
    st.markdown("""
    Notes | Country:
    - Country 5: Best results, with 83.13% of deals won, indicating strong performance.
    - Country 2: Worst results, with 57.05% of opportunities lost, reflecting poor performance.
    - Country 1: Moderate results, with 59.23% of deals won, indicating average performance.
    - Insight: The data suggests that Country 5 is the strongest performer in numer of deals, while Country 2 requires attention to improve its conversion rates. 
    Country 1 shows average results, indicating potential for growth with targeted strategies.
    """)

    
    ### -----------  Segment --------------
    st.subheader('Segment')
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_segment.pkl"], use_container_width=True)
    with col2:
        st.plotly_chart(graphics["fig_wl_segment_pct.pkl"], use_container_width=True) 
    
    # Add notes:
    st.markdown("""
    Notes | Segments:
    - Segment 1: 46.27% LOST vs. 29.58% WON – Dominates in LOST opportunities, indicating potential for improvement.
    - Segment 2: 25.13% LOST vs. 33.41% WON – Shows balanced performance, with a higher proportion of WON deals. This represents the Segment that we have better performance among the segments
    """)
    
    
    ### -----------  Time Analysis in Number --------------
    
    st.subheader('Time Analysis')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_month.pkl"], use_container_width=True)
        st.plotly_chart(graphics["fig_wl_quarter.pkl"], use_container_width=True)
        
    with col2:
        st.plotly_chart(graphics["fig_wl_month_pct.pkl"], use_container_width=True)
        st.plotly_chart(graphics["fig_wl_quarter_pct.pkl"], use_container_width=True)
    
    # Add notes:
    st.markdown("""
    Notes | Time Analysis:
    - The month with more deals closed WON was March (4553 deals), representing 59.1% of the deals closed in the month. Followed by September (4166) (54.2%) and June (4091) (54.2%)
    - In percentage february was the best, followed by March and April.

    - In terms of Total Numer of deals, the best Quarter is the Q1, with 11.7K deals WONs
    - Proportionaly, the Q2 is better, with 54.9% deals WON

    - January was the month with most LOSTs (5728), representing (59.4% of the deals closed on the month)
    - In terms of Total Number of Deals and Proportionaly, the Q4 is the worse quarter. With 10.893 deals Lost, representing 53.3% of the total in the quarter
    """)
    
    ### -----------  Time Analysis in EUR (€) --------------
    
    st.subheader('Time Analysis in EUR (€)')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_month_value.pkl"], use_container_width=True)
        st.plotly_chart(graphics["fig_quarter_value.pkl"], use_container_width=True)
        
    with col2:
        st.plotly_chart(graphics["fig_month_value_pct.pkl"], use_container_width=True)
        st.plotly_chart(graphics["fig_quarter_value_pct.pkl"], use_container_width=True)
    
    # Add notes:
    st.markdown("""
    Notes | Time Analysis in EUR (€):
    - Here we have similar comparisions, but in monetary terms.
    """)
    
    
    ### -----------  Business Type --------------
    st.subheader('Type of Business')
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_type_business_count.pkl"], use_container_width=True)
    with col2:
        st.plotly_chart(graphics["fig_wl_type_business_pct.pkl"], use_container_width=True) 
        
    # Add notes:
    st.markdown("""
    Notes | Business type:
    - Overall, the majority of opportunities stem from Existing Business.
    - Among WON opportunities, 79.78% are from Existing Business, while 20.21% come from New Business.
    - Among LOST opportunities, 75.55% are from Existing Business, with 22.68% coming from New Business. The difference between WON and LOST opportunities is minimal.
    - This suggests that Existing Business plays a crucial role in both successful and unsuccessful deals, with a slight advantage in winning opportunities.
    """)
    
     
    ### -----------  Lead Source --------------
    st.subheader('Lead Source')
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_lead_source.pkl"], use_container_width=True)
    with col2:
        st.plotly_chart(graphics["fig_wl_lead_source_pct.pkl"], use_container_width=True) 
        
    # Add notes:
    st.markdown("""
    Notes | Lead Source:
    Note that we have a lot of Unknow data in Lead Source, however we bring the numbers that we have for abalysis:
    - Top 3 WON: Referral, Sales Visit/Demo, Customer Events (!)
    - Top 3 LOST:Referral, Sales Visit/Demo, Field Service.
    """)
    
    # Add notes:
    st.markdown("""
    **Summary | WON vs. LOST Profiles**
    
    **WONs:**
    - **Segments:** WONs are most frequent in **Segment 2**, with 33.41% WON vs. 25.13% LOST.
    - **Month:** The highest number of WONs occurred in **March**, accounting for 59.1% of deals closed that month, followed by **September** and **June**.
    - **Quarter:** **Q1** had the highest total number of WONs, with 11.7K deals, while **Q2** had the highest proportional rate, with 54.9% of deals being WON.
    - **Accounts:** **Top 1 Accounts** had a significantly higher WON rate of 61.02% compared to their LOST rate of 38.98%, indicating better success with larger accounts.
    - **Country:** **Country 5** showed the best performance with 83.13% of deals WON, leading to strong results.
    - **Business Type:** **Existing Business** accounted for 79.78% of WONs, suggesting it plays a dominant role in successful deals.
    - **Lead Source:** **Referrals**, **Sales Visits/Demos**, and **Customer Events** were the leading sources of WON deals.
    
    **LOSTs:**
    - **Segments:** LOSTs were most frequent in **Segment 1**, with 46.27% LOST vs. 29.58% WON, indicating room for improvement in this segment.
    - **Month:** The highest number of LOSTs occurred in **January**, with 59.4% of deals closed being LOST.
    - **Quarter:** **Q4** had the highest total LOSTs, with 10.89K deals, and 53.3% of the deals in that quarter were LOST, reflecting poor performance.
    - **Accounts:** **Small Accounts** had the highest proportion of LOST deals, with 51.89% LOST compared to 48.11% WON, highlighting challenges in closing deals with smaller accounts.
    - **Country:** **Country 2** showed the worst results, with 57.05% of opportunities LOST, indicating poor performance in this region.
    - **Business Type:** **Existing Business** also played a major role in LOST opportunities, making up 75.55% of LOST deals.
    - **Lead Source:** **Referrals**, **Sales Visits/Demos**, and **Field Service** were the most common sources of LOST deals.
    
    **Considerations for Forecasts:**
    If the scenario of 2025 remains similar of 2024, we:
    - We hope close more from Segment 2 in 2025;
    - ..
    """)

    
    
    st.text_area("Comment about the charts:", "Add your observations..")
    
    
# ----------- AVERAGE TICKET PAGE --------------   
elif page == "Average Ticket Analysis":
    
    st.title("Average Ticket Analysis")
    st.header('Average Ticket Analysis')
    st.markdown("""
    **Questions to address - On the average ticket per opportunity**:
    - Is there a value pattern in the lost opportunities?
    - What is the average value of the won opportunities?
    - Is the average value of the won opportunities higher or lower than that of the lost opportunities?
    """)
    
    ### -----------  GENERAL --------------
    st.subheader('General')

    # Display the stats table in Streamlit
    stats_wl_at = data.groupby('Stage')[' Opp Value (EUR)'].describe()    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_avg_ticket.pkl"], use_container_width=True)
    with col2:
        st.markdown("### Descriptive Statistics by Stage")
        st.dataframe(stats_wl_at)
        st.write("\n\n\n")
        # Add notes:
        st.markdown("""         
        **Notes | General:**
        In geraneral,
        - The LOST Opportunities have a mean of 123.97 and the stand deviation of 161, lower than Wons
        - The median of LOSTs is 61 EUR, lower than WONs (Median is better to analyse because is less sensitive to Outliers)
        - The average value of WON ops are 166.29, bigger than Losts
        - In general, the value of WON Opps are higher than LOST Opps
        """)
    
    ### -----------  DEEP DIVE BY ACCOUNT TYPE --------------
    st.subheader('Deep Dive in Account Type')

    # Display the stats table in Streamlit
    stats_wl_at_account_type = data.groupby([' Account Type', 'Stage'])[' Opp Value (EUR)'].describe()
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_avg_ticket_account_type.pkl"], use_container_width=True)
    with col2:
        st.markdown("### Descriptive Statistics by Account Type per Stage")
        st.dataframe(stats_wl_at_account_type)
        st.write("\n\n\n")
        # Add notes:
        st.markdown("""
        **Notes | Account Type:**
        - On LOST Opps, Small business have a higher mean Opp Value (EUR)
        - On WON Opps, Top 2 business have a higher mean Opp Value (EUR) - Top 2 seems to bring more value for the company, in general
        """)
        
        
    ### -----------  DEEP DIVE BY COUNTRY --------------
    st.subheader('Deep Dive in Country')

    # Display the stats table in Streamlit
    stats_wl_at_country = data.groupby(['Country', 'Stage'])[' Opp Value (EUR)'].describe()
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_avg_ticket_country.pkl"], use_container_width=True)
    with col2:
        st.markdown("### Descriptive Statistics by Contry per Stage")
        st.dataframe(stats_wl_at_country)
        st.write("\n\n\n")
        # Add notes:
        st.markdown("""
        **Notes | Country:**
        - The Mean Mean of WON Opportunities Occour on Country 1 - Mean of 211 EUR. However, is the country that we Sell less.
        - The Major Mean of LOST Opportunities Occour on Country 5 - Mean of 209 EUR; Despite this, Country 5 is where our results proportionally is better in WONs (83% are WONs)
        """)
        
    ### -----------  DEEP DIVE BY SEGMENT --------------
    st.subheader('Deep Dive in Segment')

    # Display the stats table in Streamlit
    stats_wl_at_segment = data.groupby(['Segment', 'Stage'])[' Opp Value (EUR)'].describe()
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_avg_ticket_segment.pkl"], use_container_width=True)
    with col2:
        st.markdown("### Descriptive Statistics by Segment per Stage")
        st.dataframe(stats_wl_at_segment)
        st.write("\n\n\n")
        # Add notes:
        st.markdown("""
        **Notes | Country:**
        - On WON opportunities, Segment 4 represents the highest mean, with 233.90 EUR, suggesting that this segment has higher-value deals when successfully closed. Segment 4 has the highest variability (std 270.07 EUR for Won), which suggests that deals in this segment might range from very small to extremely large values.
        - Segment 1 has the highest mean among LOST opportunities (127.18 EUR), meaning that this segment represents the largest volume of lost deals in terms of value.
        """)



# ----------- AVARAGE TIME PAGE --------------

elif page == "Average Time to Close":
    st.title("Average Time to Close")
    st.header('Average Time to Close Analysis')
    st.markdown("""
    **Questions to address - On the average time taken to close the opportunity**:
    - What is the average time for won opportunities and lost opportunities?
    - What is the difference between the times for won and lost opportunities?
    - Is there a pattern of lost opportunities by product type?
    """)
    
     ### -----------  GENERAL --------------
    st.subheader('General')

    # Display the stats table in Streamlit
    stats_wl_avg_time = data.groupby('Stage')['Deal Opened (Days)'].describe()  
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_avg_time.pkl"], use_container_width=True)
    with col2:
        st.markdown("### Descriptive Statistics by Stage")
        st.dataframe(stats_wl_avg_time)
        st.write("\n\n\n")
        # Add notes:
        st.markdown("""         
        **Notes | General:**
        - What is the average time for won opportunities and lost opportunities?
        In general:
        - Closed Lost	~ 76 days
        - Closed Won - ~ 35 days
        
        What is the difference between the times for won and lost opportunities?
        - The mean duration for won opportunities differs from that of lost opportunities by 40 days. This suggests that when an opportunity remains open for too long, the chances of it not closing successfully—or taking longer to close—increase.
        - It is more expressive for small opportunities
        - Among the different Account Types, 'Top2' has the shortest average closing time for successful deals, at 31 days.
        """)
    
    ### -----------  DEEP DIVE BY ACCOUNT TYPE --------------
    st.subheader('Deep Dive in Account Type')

    # Display the stats table in Streamlit
    stats_wl_avg_time_account_type = data.groupby(['Stage', " Account Type"])['Deal Opened (Days)'].describe()
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_avg_time_account_type.pkl"], use_container_width=True)
    with col2:
        st.markdown("### Descriptive Statistics by Account Type per Stage")
        st.dataframe(stats_wl_avg_time_account_type)
        st.write("\n\n\n")
        # Add notes:
        st.markdown("""
        **Notes | Account Type:**
        - WON Deals Close Faster Than LOST Deals
            - The average number of days to close a WON deal is significantly lower across all account types compared to LOST deals.
            - For example, Small Accounts take 34 days (WON) vs. 80 days (LOST) on average.

        -Top 2 Accounts Have the Fastest WON Deals
            - Among WON deals, Top 2 Accounts close the fastest, with a mean of 31.06 days, followed by Top 3 (34 days) and Small Accounts (34 days).
            - This suggests that Top 2 Accounts may have a more streamlined decision-making process or higher deal urgency.
        
        - Small LOST Accounts Take the Longest to Close:
            - Small Accounts have the highest average duration for LOST deals (80 days). This could indicate higher indecision or more budget constraints.
        
        - Higher Standard Deviation in LOST Deals Suggests Unpredictability, possibly due to prolonged negotiations or reconsiderations deals.
            
        """)
        
        
    ### -----------  DEEP DIVE BY TYPE OF BUSINESS --------------
    st.subheader('Deep Dive in Existing Business')

    # Display the stats table in Streamlit
    stats_wl_avg_time_type_business = data.groupby(['Stage', "Type"])['Deal Opened (Days)'].describe()
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graphics["fig_wl_avg_time_type_business.pkl"], use_container_width=True)
    with col2:
        st.markdown("### Descriptive Statistics by Type of Business per Stage")
        st.dataframe(stats_wl_avg_time_type_business)
        st.write("\n\n\n")
        # Add notes:
        st.markdown("""
        **Notes | Type of Business:**
        - In LOST opportunities, New Business deals take an average of 104 days to close, whereas Existing Business deals take 58 days on average. This suggests that new business opportunities tend to remain open for longer before being lost, potentially indicating higher uncertainty, longer decision-making processes, or greater difficulty in conversion compared to existing clients.
        - Additionally, salespeople tend to receive a lost decision faster from existing business accounts than from new business accounts, making forecasts for existing business opportunities faster compared to new business.
        """)
    

 
# ----------- PREDICTION PAGE -------------- 
   
elif page == "Prediction":
    st.title("Stage Prediction")
    
    
# ----------- AGENT PAGE --------------    
    
elif page == "Agent Assistant":
    st.title("Agent Assistant")
