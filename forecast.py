import streamlit as st
import joblib
from datetime import datetime 
import math
from dateutil.relativedelta import relativedelta
import pandas as pd
import calendar
import plotly.figure_factory as ff
import plotly.express as px


col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('images/airplane.png', width=80)
with col2:
    st.title("Plan your next holiday")

st.write( """
         Are you ready to take off on your next adventure, 
         and want to make sure you travel at a time when you &mdash; and your travel companions are **least exposed to harmful air quality**?
        """ )
    
model = joblib.load('sarima_model.pkl')

st.selectbox('📌 Choose your location', ['Los Angeles', 'More locations - coming soon'])

col1, col2 = st.columns(2)
next_two_year = [2024, 2025, 2026]

month_key_value =  {
        'January': 1,
        'February' : 2,
        'March': 3,
        'April': 4,    
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

selectedMonth = col1.selectbox(
    '📅 Choose the month..',
    month_key_value.keys())

selectedYear = col2.selectbox("..and the year", next_two_year)

day = datetime(year=selectedYear, month = month_key_value[selectedMonth] , day=1)

prediction = model.predict(start=day, end=day)
value = math.ceil(prediction.values[0])

st.subheader("How air quality is going to be?")

if (value < 100):
    c = f'{value}'
    message = '##### This air quality is suitable for all individuals.'
    image = ('images/confetti.png')
else: 
    c = f'{value}'
    message = '##### This air quality is not suitable for all individuals.'
    image = ('images/speedometer.png')

col1, mid, col2 = st.columns([1,1,15])
with col1:
    st.image(image, width=60)
with col2:
    st.write(f'##### The predicted air quality for {selectedMonth} {selectedYear} is {c}.')
    st.write(message)

st.subheader("What does it mean for your health?")

if (value <= 50):
    st.write("This air quality value is **good** &mdash; it means it's safe for everyone.")
if (value > 50 and value <= 100):
    # st.image('images.png')
    st.write("This air quality value is **moderate** &mdash; it means it's safe for most people, but those very sensitive to the air quality might experience some symptoms.")
if (value > 100 and value <= 150):
    st.write("This air quality value is **unhealthy for sensitive groups** &mdash; it means it's not safe for sensitive individuals.")
if (value > 150 and value <= 200):
    st.write("This air quality value is **unhealthy** &mdash; it means it's not safe for most people, especially those in the high-risk groups.")
if (value > 200 and value <= 300):
    st.write("This air quality value is ** very unhealthy** &mdash; it means it might cause health problems in most individuals.")
if (value > 300):
    st.write('Haradous')

series = model.predict(start=day, end= day + relativedelta(months = 5))
# st.write(series.values)
months_name = []
for x in series.index:
    months_name.append(calendar.month_name[x.month])


def convertToMonth(li) :
    month_names = []
    for x in li:
        month_names.append(calendar.month_name[x])
    return month_names     

df = series.to_frame()
data = pd.DataFrame(data=series.values, columns=['AQI'])
data['Date'] = series.index
data["Month"] = convertToMonth(pd.DatetimeIndex(data['Date']).month)

st.subheader("Is there a better time to travel in the next 6 months?")

col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('images/q.png', width=80)
with col2:
    st.write("""
        Wonder if there's a better time to travel to your desired destination in the next 6 months?
        You can check in the graph below whether air quality is set to increase or decrease in the next 6 months from your desired dates.
             """)

i = data['AQI'].idxmin()

fig = px.line(y=data['AQI'], x=data['Month'], color_discrete_sequence=('#6A8D73', '#5E4C5A'))
fig.add_vrect(x0=data.index[i], x1=data.index[i], line_width=60, fillcolor='#FFE8C2', opacity=0.2, annotation_text="lowest monthly values")
fig.update_layout(
    yaxis_title='Air Quality Index (AQI)',
    xaxis_title='Month',
    title='Air quality index for the next 6 month')
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write("""
        The month highlighted in the graph is the month with the lowest air quality values &mdash; 
         that means it has the highest air quality in the next 6 months.
             """)