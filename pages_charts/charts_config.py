import plotly.express as px
import pandas as pd
import os
print("Current working directory:", os.getcwd())

def load_and_process_data():
    # Load the data from one directory level up
    data = pd.read_csv("data/sales_preprocessed_data.csv")

    # Convert date columns to datetime
    data["Created Date"] = pd.to_datetime(data["Created Date"], errors="coerce")
    data["Close Date"] = pd.to_datetime(data["Close Date"], errors="coerce")

    return data

data = load_and_process_data()

elegant_colors = [
    "#1F77B4",  # Muted Blue
    "#FF7F0E",  # Soft Orange
    "#17BECF",  # Light Cyan
    "#2CA02C",  # Deep Green
    "#D62728",  # Dark Red
    "#9467BD",  # Muted Purple
    "#8C564B",  # Warm Brown
    "#E377C2",  # Soft Pink
    "#7F7F7F",  # Neutral Gray
    "#BCBD22",  # Olive Green
    "#AEC7E8",  # Light Blue
    "#FFBB78",  # Peach
    "#98DF8A",  # Light Green
    "#FF9896",  # Light Red
    "#C5B0D5"   # Soft Lavender
]

colors_won_vs_lost = [
    "#D62728",  # Dark Red
    "blue",  # Muted Blue
]

if __name__ == "__main__":
    # This will execute when the script is run directly
    data = load_and_process_data()
    print(data.head())  # You can replace this with other code you need to execute
