import streamlit as st
import joblib
from datetime import datetime 
import math
from dateutil.relativedelta import relativedelta
import pandas as pd
import calendar
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px


st.write("# Let's have a look at the data..")

### A. define function to load data
def load_data(path):

    df = pd.read_csv(path, index_col='Date', parse_dates=True)
     
    return df

data = load_data("cleaned_aqi.csv")

st.subheader('Overall trends are promising')

st.markdown("""
            Things are going in the right direction. Air quality index is dropping, which means cleaner air and less health risk. That's great news.
            """)

air_quality_yearly = data.groupby('Year')['AQI'].mean()

fig = px.line(air_quality_yearly, y=air_quality_yearly.values, x=air_quality_yearly.index, color_discrete_sequence=('#6A8D73', '#5E4C5A'))
fig.update_layout(
    yaxis_title='Air Quality Index (AQI)',
    title='Air Quality Index - Yearly averages from 1980 to 2021')

st.plotly_chart(fig, theme='streamlit', use_container_width=True)

st.write("# All months are made equal?!")

st.write('#### No, in short &mdash; they are not.')

st.markdown("""
            Summer months seem to have worst air quality on average, while the air is generally cleaner during the winter months.
            """)

air_quality_monthly_avg = data.groupby('Month')['AQI'].mean()
monthly_mean_diff = ((air_quality_monthly_avg - air_quality_monthly_avg.mean())/air_quality_monthly_avg)

# Plotting

fig = px.bar(monthly_mean_diff, color_discrete_sequence=('#6A8D73', '#5E4C5A'))
fig.update_layout(
    yaxis_title='Difference (%)',
    yaxis_tickformat = '0.2%',
    title='Difference from monthly averages per month')
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write("# What about your health?")

st.write('#### The lower, the better.')

st.markdown("""
            Air quality index ranges from 0 to 300 (or higher values) and lower values mean cleaner air &mdash; and less health risk.  \n  \n Click on the ranges below to see what they mean for the human health.  
            """)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["0-50", "51-100", "101-150", "151-200", "201-300", "301 or higher"])

with tab1:
    col1, mid, col2 = st.columns([1,1,70])
    with col1:
        st.image('images/good.png', width=25)
    with col2:
        st.write("##### Category: Good")
    st.write("Air quality is satisfactory, and air pollution poses little or no risk.")

with tab2:
    col1, mid, col2 = st.columns([1,1,70])
    with col1:
        st.image('images/moderate.png', width=25)
    with col2:
        st.write("##### Category: Moderate")
    st.write("Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.")

with tab3:
    col1, mid, col2 = st.columns([1,1,70])
    with col1:
        st.image('images/sensitive.png', width=25)
    with col2:
        st.write("##### Category: Unhealthy for sensitive groups")   
    st.write("Members of sensitive groups may experience health effects. The general public is less likely to be affected.")

with tab4:
    col1, mid, col2 = st.columns([1,1,70])
    with col1:
        st.image('images/unhealthy.png', width=25)
    with col2:
        st.write("##### Category: Unhealthy")
    st.write("Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.")

with tab5:
    col1, mid, col2 = st.columns([1,1,70])
    with col1:
        st.image('images/very_unhealthy.png', width=25)
    with col2:
        st.write("##### Category: Very unhealthy")
    st.write("Health alert: The risk of health effects is increased for everyone.")

with tab6:
    col1, mid, col2 = st.columns([1,1,70])
    with col1:
        st.image('images/hazardous.png', width=25)
    with col2:
        st.write("##### Category: Hazardous")
    st.write("Health warning of emergency conditions: everyone is more likely to be affected.")

data['season'] = data['Month'].map({12: 'winter', 
                                        1: 'winter', 
                                        2: 'winter',
                                        3: 'spring',
                                        4: 'spring',
                                        5: 'spring',
                                        6: 'summer',
                                        7: 'summer',
                                        8: 'summer',
                                        9: 'autumn',
                                        10: 'autumn',
                                        11: 'autumn'})

st.write("#### Choose a year to to see how many days of clean air it had.")

year = st.select_slider(
    "**Year**",
    options=data['Year'])

if year:
    data = data[data['Year'] == year]

fig = px.histogram(x=data['city_ascii'], color=data['Category'], 
                   color_discrete_map={
                       'Unhealthy': '#FE654F',
                       'Unhealthy for Sensitive Groups': '#D68D1F', 
                       'Moderate': '#FFE8C2', 
                       'Good': '#6A8D73', 
                       'Very Unhealthy': '#5E4C5A', 
                       'Hazardous': '#0D1321'})
fig.update_layout(
    yaxis_title='Count of days in each category',
    xaxis_title = 'Season',
    title='On most days air quality is moderate')
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write("##### Want to know more?")

st.markdown("""
            Let's see how different seasons affect air quality. Go to the next page to find out more.
            """)