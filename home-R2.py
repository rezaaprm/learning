# Import Dashboard Library
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

# Library Tambahan
import time
from streamlit_extras.let_it_rain import rain 
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Library Visualization
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Library Manipulation Data
import pandas as pd 
import numpy as np 

# Config Web Streamlit
st.set_page_config(page_title="Video Games Sales", layout="wide")
st.snow()
st.toast("🎮")

def example():
    rain(
        emoji="☀️",
        font_size=3,
        falling_speed=3,
        animation_length="infinite",
    )
example()

with st.spinner("Please Wait..."):
    time.sleep(3)


# Container-Header
st.markdown("## Dashboard of Video Games Sales using Streamlit Framework")

# Dataset
try:
    dataset = pd.read_csv("vgsales.csv")
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}. Pastikan file 'vgsales.csv' tersedia.")
    st.stop()

# Calculate Global-Sales
df = dataset[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].aggregate("sum").sort_values(ascending=True).reset_index()
df.columns = ["Region", "Sales"]

# Container-Global_Sales
add_vertical_space(2)
st.info("Exploration Data Analysis on Global Sales")
col1, col2 = st.columns([0.5, 0.5], gap="small")

with col1:
    fig = px.bar(df, y="Region", x="Sales", text_auto='.4s')
    fig.update_traces(marker_color=px.colors.sequential.Brwnyl)
    fig.update_layout(title="Sum of Games Sales by Regions", xaxis_title="", yaxis_title="", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(df, values="Sales", names="Region", hole=0.5, color_discrete_sequence=px.colors.sequential.Magenta_r)
    fig.update_traces(textinfo="percent")
    fig.update_layout(title="Percentage of Games Sales by Regions", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)


# Additional (Stack Bar dengan Arsiran Tipis + Line Chart Multi-Track Per Region)
col1, col2 = st.columns([0.5, 0.5], gap="small")

with col1:
    df_platform = dataset.groupby("Platform")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum").reset_index()
    df_platform = df_platform.sort_values(by="Global_Sales", ascending=False).head(5)

    regions = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
    patterns = ["/", "x", "+", "-"] # Jenis arsiran/pola

    fig = go.Figure()

    for region, pattern in zip(regions, patterns):
        fig.add_trace(go.Bar(
            x=df_platform["Platform"], 
            y=df_platform[region], 
            name=region.replace('_', ' '), 
            marker=dict(
                pattern_shape=pattern,
                pattern_solidity=0.3  # <-- Nilai ini mengecilkan/menipiskan arsiran agar tidak tebal/silau
            )
        ))
        
    fig.update_layout(
        barmode="stack", 
        title="Sales by Platform and Region (Stacked with Thin Patterns)", 
        xaxis_title="Platform", 
        yaxis_title="Sales (juta unit)", 
        template="plotly_dark",
        yaxis=dict(rangemode="tozero")
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Line chart dibuat detail (multi-track) berdasarkan masing-masing Region
    df_yearsales_region = dataset.groupby("Year")[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].aggregate("sum").reset_index()
    
    df_melted_year = df_yearsales_region.melt(
        id_vars='Year',
        value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
        var_name='Region',
        value_name='Sales'
    )
    df_melted_year['Region'] = df_melted_year['Region'].str.replace('_Sales', '')

    fig = px.line(
        df_melted_year, 
        x="Year", 
        y="Sales", 
        color="Region", # Membuat multi-track line chart berdasarkan region
        markers=True,
        title="Sales Trend by Region Over Years (Multi-Track)"
    )
    fig.update_layout(template="plotly_dark", yaxis=dict(rangemode="tozero"))
    st.plotly_chart(fig, use_container_width=True)


# Divider
st.info("Analyze of Best Games Names, Publisher, Genre, and Platform on Global Sales")
# Single Bar Chart
col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25], gap="small")

# Calculate by Platform
with col1:
    df = dataset.groupby("Platform")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum").reset_index()
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = px.bar(df, y="Platform", x="Global_Sales", text_auto='.4s')
    fig.update_traces(marker_color=px.colors.sequential.Bluyl_r)
    fig.update_layout(title="Best of Platforms by Regions", xaxis_title="", yaxis_title="", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Calculate by Genre
with col2:
    df = dataset.groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum").reset_index()
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = px.bar(df, y="Genre", x="Global_Sales", text_auto='.4s')
    fig.update_traces(marker_color=px.colors.sequential.Bluyl_r)
    fig.update_layout(title="Best of Genres by Regions", xaxis_title="", yaxis_title="", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Calculate by Publisher
with col3:
    df = dataset.groupby("Publisher")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum").reset_index()
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = px.bar(df, y="Publisher", x="Global_Sales", text_auto='.4s')
    fig.update_traces(marker_color=px.colors.sequential.Bluyl_r)
    fig.update_layout(title="Best of Publishers by Regions", xaxis_title="", yaxis_title="", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Calculate by Name
with col4:
    df = dataset.groupby("Name")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum").reset_index()
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = px.bar(df, y="Name", x="Global_Sales", text_auto='.4s')
    fig.update_traces(marker_color=px.colors.sequential.Bluyl_r)
    fig.update_layout(title="Best of Games by Regions", xaxis_title="", yaxis_title="", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)


# Group Bar Row Chart (Make Subplots)
col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25], gap="small")

with col1:
    df = dataset.groupby("Platform")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)
    
    fig = make_subplots(rows=4, cols=1, shared_yaxes=True)
    fig.add_trace(go.Bar(y=df.Platform, x=df.NA_Sales, name="North America", orientation='h'), 1, 1)
    fig.add_trace(go.Bar(y=df.Platform, x=df.EU_Sales, name="Europe", orientation='h'), 2, 1)
    fig.add_trace(go.Bar(y=df.Platform, x=df.JP_Sales, name="Japanese", orientation='h'), 3, 1)
    fig.add_trace(go.Bar(y=df.Platform, x=df.Other_Sales, name="Others", orientation='h'), 4, 1)

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Top 5 Platforms by Global Sales Figures", xaxis_title="", yaxis_title="", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    df = dataset.groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)
    
    fig = make_subplots(rows=4, cols=1, shared_yaxes=True)
    fig.add_trace(go.Bar(y=df.Genre, x=df.NA_Sales, name="North America", orientation='h'), 1, 1)
    fig.add_trace(go.Bar(y=df.Genre, x=df.EU_Sales, name="Europe", orientation='h'), 2, 1)
    fig.add_trace(go.Bar(y=df.Genre, x=df.JP_Sales, name="Japanese", orientation='h'), 3, 1)
    fig.add_trace(go.Bar(y=df.Genre, x=df.Other_Sales, name="Others", orientation='h'), 4, 1)

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Best Genre by Regions", xaxis_title="", yaxis_title="", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    df = dataset.groupby("Publisher")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = make_subplots(rows=4, cols=1, shared_yaxes=True)
    fig.add_trace(go.Bar(y=df.Publisher, x=df.NA_Sales, name="North America", orientation='h'), 1, 1)
    fig.add_trace(go.Bar(y=df.Publisher, x=df.EU_Sales, name="Europe", orientation='h'), 2, 1)
    fig.add_trace(go.Bar(y=df.Publisher, x=df.JP_Sales, name="Japanese", orientation='h'), 3, 1)
    fig.add_trace(go.Bar(y=df.Publisher, x=df.Other_Sales, name="Others", orientation='h'), 4, 1)

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Best Publisher by Regions", xaxis_title="", yaxis_title="", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    df = dataset.groupby("Name")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = make_subplots(rows=4, cols=1, shared_yaxes=True)
    fig.add_trace(go.Bar(y=df.Name, x=df.NA_Sales, name="North America", orientation='h'), 1, 1)
    fig.add_trace(go.Bar(y=df.Name, x=df.EU_Sales, name="Europe", orientation='h'), 2, 1)
    fig.add_trace(go.Bar(y=df.Name, x=df.JP_Sales, name="Japanese", orientation='h'), 3, 1)
    fig.add_trace(go.Bar(y=df.Name, x=df.Other_Sales, name="Others", orientation='h'), 4, 1)

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Best Games by Regions", xaxis_title="", yaxis_title="", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)


# Group Bar Chart
col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25], gap="small")

with col1:
    df = dataset.groupby("Platform")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df["Platform"], x=df["NA_Sales"], name="North America", orientation='h'))
    fig.add_trace(go.Bar(y=df["Platform"], x=df["EU_Sales"], name="Europe", orientation='h'))
    fig.add_trace(go.Bar(y=df["Platform"], x=df["JP_Sales"], name="Japanese", orientation='h'))
    fig.add_trace(go.Bar(y=df["Platform"], x=df["Other_Sales"], name="Others", orientation='h'))

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Top 5 Platforms by Global Sales Figures", xaxis_title="Sales", yaxis_title="Platform", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    df = dataset.groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df["Genre"], x=df["NA_Sales"], name="North America", orientation='h'))
    fig.add_trace(go.Bar(y=df["Genre"], x=df["EU_Sales"], name="Europe", orientation='h'))
    fig.add_trace(go.Bar(y=df["Genre"], x=df["JP_Sales"], name="Japanese", orientation='h'))
    fig.add_trace(go.Bar(y=df["Genre"], x=df["Other_Sales"], name="Others", orientation='h'))

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Best Genre by Regions", xaxis_title="Sales", yaxis_title="Genre", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col3:
    df = dataset.groupby("Publisher")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df["Publisher"], x=df["NA_Sales"], name="North America", orientation='h'))
    fig.add_trace(go.Bar(y=df["Publisher"], x=df["EU_Sales"], name="Europe", orientation='h'))
    fig.add_trace(go.Bar(y=df["Publisher"], x=df["JP_Sales"], name="Japanese", orientation='h'))
    fig.add_trace(go.Bar(y=df["Publisher"], x=df["Other_Sales"], name="Others", orientation='h'))

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Best Publisher by Regions", xaxis_title="Sales", yaxis_title="Publisher", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    df = dataset.groupby("Name")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
    df = df.sort_values(by=["Global_Sales"]).reset_index().tail(5)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df["Name"], x=df["NA_Sales"], name="North America", orientation='h'))
    fig.add_trace(go.Bar(y=df["Name"], x=df["EU_Sales"], name="Europe", orientation='h'))
    fig.add_trace(go.Bar(y=df["Name"], x=df["JP_Sales"], name="Japanese", orientation='h'))
    fig.add_trace(go.Bar(y=df["Name"], x=df["Other_Sales"], name="Others", orientation='h'))

    fig.update_traces(marker_color=px.colors.sequential.algae_r)
    fig.update_layout(title="Best Games by Regions", xaxis_title="Sales", yaxis_title="Games", barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)