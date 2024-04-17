from st_pages import Page, show_pages, add_page_title
import streamlit as st

st.image('images/welcome.jpg')

st.write("# Welcome to my capstone project. ")

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be

show_pages(
    [
        Page("welcome.py", "Introduction", "👋"),
        Page("trends.py", "Trends", "📊"),
        Page("seasonal.py", "Seasonality", ":🍃:"),
        Page("forecast.py", "Forecast", ":partly_sunny_rain:"),
        Page("contact.py", "Let's connect", "💬")        
    ]
)

st.markdown(
    """
This is my capstone project submission for BrainStation's Data Science programe.
""")

st.write("#### Problem statement")

st.write("""
It is estimated that 90% of the world's population live in places with bad air quality. 
Poor air quality has adverse health affects on human, which means lower life quality and expectancy, and higher healthcare costs. 

This is especially true for sensitive groups, i.e. children, elderly, and people with pre-excisting lung and heart conditions. 
These groups are at a higher risk of adverse health effects even at less harmful levels of bad air quality. 
This project aims at providing a solution to these high-risk groups to empower them minimize their risk to bad air quality by providing accurate forecasts and allow them to plan their outdoor time accordingly.      
""")

st.write("#### What can we do about it?")


st.write("""
         Establishing a model that provides accurate forecasts could improve awereness and engagement with the topic, which in turn could help facilitate a change for the better. 
         """)

st.write('#### Conext')

st.write("""
         To maximize potential reach and get this project off the ground, a location with a high public interest in the topic is chosen: 45% of residents in Los Angeles think that air quality is a 'big problem'.
Moreover, the region has been ranked as the 4th most polluted city in the US, therefore improvement measures would be highly beneficial.
         """)