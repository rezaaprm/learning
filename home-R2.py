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
st.set_page_config(page_title="Video Games Sales Dashboard", layout="wide")
st.balloons()

def example():
    rain(
        emoji="☀️",
        font_size=3,
        falling_speed=3,
        animation_length="infinite",
    )
example()

with st.spinner("Please Wait..."):
    time.sleep(2)

# Container-Header
st.markdown("## Dashboard of Video Games Sales using Streamlit Framework")

# Dataset
try:
    dataset = pd.read_csv("vgsales.csv")
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}. Pastikan file 'vgsales.csv' tersedia.")
    st.stop()

# Calculate Global-Sales
df_region = dataset[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].aggregate("sum").sort_values(ascending=True).reset_index()
df_region.columns = ["Region", "Sales"]

# Container-Global_Sales
add_vertical_space(1)
st.info("Exploration Data Analysis on Global Sales")
col1, col2 = st.columns(2, gap="small")

with col1:
    fig = px.bar(df_region, y="Region", x="Sales", text_auto='.4s')
    fig.update_traces(marker_color=px.colors.sequential.Brwnyl)
    fig.update_layout(title="Sum of Games Sales by Regions", xaxis_title="", yaxis_title="", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(df_region, values="Sales", names="Region", hole=0.5, color_discrete_sequence=px.colors.sequential.Magenta_r)
    fig.update_traces(textinfo="percent")
    fig.update_layout(title="Percentage of Games Sales by Regions", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)


# Additional Section (Perbaikan: Mengganti Stacked ber-arsiran dengan Grouped Bar yang Bersih)
col1, col2 = st.columns(2, gap="small")

with col1:
    df_platform = dataset.groupby("Platform")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum").reset_index()
    df_platform = df_platform.sort_values(by="Global_Sales", ascending=False).head(5)
    
    # Melt dataframe agar mudah dijadikan grouped bar chart yang bersih tanpa arsiran silau
    df_melted = df_platform.melt(
        id_vars='Platform',
        value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
        var_name='Region',
        value_name='Sales'
    )
    df_melted['Region'] = df_melted['Region'].str.replace('_Sales', '')

    fig = px.bar(
        df_melted,
        x='Platform',
        y='Sales',
        color='Region',
        barmode='group',
        title="Top 5 Platforms Sales by Region",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_layout(template="plotly_dark", yaxis=dict(rangemode="tozero"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    df_yearsales = dataset.groupby("Year")[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].aggregate("sum").reset_index()
    
    fig = px.line(
        df_yearsales, 
        x="Year", 
        y="Global_Sales", 
        markers=True,
        color_discrete_sequence=px.colors.sequential.Agsunset_r
    )
    fig.update_layout(title="Global Sales Trend Over Years", template="plotly_dark", yaxis=dict(rangemode="tozero"))
    st.plotly_chart(fig, use_container_width=True)


# Divider
st.info("Analyze of Best Games Names, Publisher, Genre, and Platform on Global Sales")

# Top 5 Performance Overview (Clean Single Bar Charts)
col1, col2, col3, col4 = st.columns(4, gap="small")

categories = [("Platform", col1), ("Genre", col2), ("Publisher", col3), ("Name", col4)]

for col_name, col_obj in categories:
    with col_obj:
        df_top = dataset.groupby(col_name)[["Global_Sales"]].aggregate("sum").reset_index()
        df_top = df_top.sort_values(by="Global_Sales", ascending=True).tail(5)

        fig = px.bar(df_top, y=col_name, x="Global_Sales", text_auto='.4s', orientation='h')
        fig.update_traces(marker_color=px.colors.sequential.Bluyl_r)
        fig.update_layout(
            title=f"Top 5 {col_name}s", 
            xaxis_title="", 
            yaxis_title="", 
            template="plotly_dark",
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)


# Group Bar Chart (Perbaikan Syntax Error / Tuple Bug dari Kode Sebelumnya)
st.info("Detailed Regional Breakdown by Category")
col1, col2, col3, col4 = st.columns(4, gap="small")

categories_detailed = [("Platform", col1), ("Genre", col2), ("Publisher", col3), ("Name", col4)]

for col_name, col_obj in categories_detailed:
    with col_obj:
        df_det = dataset.groupby(col_name)[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].aggregate("sum")
        df_det = df_det.sort_values(by="Global_Sales", ascending=True).tail(5).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(y=df_det[col_name], x=df_det["NA_Sales"], name="North America", orientation='h'))
        fig.add_trace(go.Bar(y=df_det[col_name], x=df_det["EU_Sales"], name="Europe", orientation='h'))
        fig.add_trace(go.Bar(y=df_det[col_name], x=df_det["JP_Sales"], name="Japanese", orientation='h'))
        fig.add_trace(go.Bar(y=df_det[col_name], x=df_det["Other_Sales"], name="Others", orientation='h'))

        fig.update_traces(marker_color=px.colors.sequential.algae_r)
        fig.update_layout(
            title=f"Regional Breakdown by {col_name}",
            xaxis_title="Sales",
            yaxis_title=col_name,
            barmode='group',
            template="plotly_dark",
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)