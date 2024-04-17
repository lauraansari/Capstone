# Loading librariesr
import streamlit as st
import joblib
from datetime import datetime 
import math
from dateutil.relativedelta import relativedelta
import pandas as pd
import calendar
import plotly.figure_factory as ff
import plotly.express as px

# Loading data
def load_data(path):

    df = pd.read_csv(path, index_col='Date', parse_dates=True)
     
    return df

data = load_data("cleaned_aqi.csv")


st.write("# So how do different seasons affect air quality?  \n")

st.write('##### Find out how the daily values of air quality index change over the different seasons.')

st.write("""

         """)

col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('images/season2.png', width=80)
with col2:
    st.write('''
             The air quality is affected by the time of the year we're in.  \n This means that the air quality in the summer is **distinctly different** from the winter. It's not a causal relationship &mdash; but a relationship do exist.''')

data['Health risks'] = data['Category'].map({'Hazardous': 'Health risk', 
                                        'Good': 'No risk', 
                                        'Unhealthy': 'Health risk',
                                        'Very Unhealthy': 'Health risk',
                                        'Unhealthy for Sensitive Groups': 'Health risk',
                                        'Moderate': 'No risk'})

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

st.sidebar.subheader("Choose the season")
spring = st.sidebar.checkbox('Spring')
summer = st.sidebar.checkbox('Summer')
autumn = st.sidebar.checkbox('Autumn')
winter = st.sidebar.checkbox('Winter')

if spring:
    data = data[data['season'] == 'spring']

if summer:
    data = data[data['season'] == "summer"]

if autumn:
    data = data[data['season'] == 'autumn']

if winter:
    data = data[data['season'] == 'winter']

air_quality_mean = pd.DataFrame(data.groupby('Day')['AQI'].mean())
air_quality_std = pd.DataFrame(data.groupby('Day')['AQI'].std())
air_quality_std.rename(columns={'AQI': 'Standard deviation'}, inplace=True)
air_quality_daily = pd.concat([air_quality_mean, air_quality_std], axis=1)

fig = px.line(air_quality_daily, x=air_quality_daily.index, y=['AQI'], color_discrete_sequence=('#6A8D73', '#5E4C5A'))
fig.update_layout(
    yaxis_title='Frequency',
    title='Average daily values of AQI')
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write("# How does it affect sensitive individuals?")

st.write('#### Health risks are different for sensitive individuals.')

st.write('''
         If you're a sensitive individual, you might be more affected by air quality than the general public.
         The below chart shows the number of risk-free and risky days on average, in a year.

''')

fig = px.bar(data['Health risks'].value_counts().sort_values()/data['Year'].nunique(), color_discrete_sequence=('#6A8D73', '#5E4C5A'))
fig.update_layout(
    showlegend=False,
    yaxis_title='Number of days inr the category',
    title='Frequency of the air quality categories')
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write("# What's the major contributor to air pollution?")

st.write("#### It's changing by the season, too.")

st.write('''
         There are many air pollutants out there. 
         You might be more sensitive to some than others &mdash; so it's important to know what's out there in the different seasons.''')

fig = px.pie(values=data['Defining Parameter'].value_counts().sort_values(), 
             names=data['Defining Parameter'].value_counts().index, 
             color_discrete_sequence=('#6A8D73', '#172815', '#FFE8C2', '#5E4C5A', '#F4EDEA'))
fig.update_layout(
    yaxis_title='Frequency',
    title='Frequency of the air quality categories')
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write("##### Ready to take off yet?")
st.write("Let's see how the air quality is going to be on that vacation you're planning.")