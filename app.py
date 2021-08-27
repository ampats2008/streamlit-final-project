"""
Name:       Anthony Medugno
CS230 - SN1
Data:       cl_used_cars_7000_sample.csv
URL:        Link to your web application online (see extra credit)

Description:

This program contains 2 different functions (i.e. queries).
1. Allows the user to filter data using Streamlit UI controls and Pandas dataframes.
    In this case the user may be a customer looking to purchase a used car based on some preferences.
    The output of this query will be displayed in a Streamlit UI table.

2. The only input on this page is to select a state on the sidebar. This page contains two different visualizations:
    A. a matplotlib bar graph that displays the most popular regions in a given state (using a dataframe that groups by
    region and counts the number of listings in each region.
    B. a PyDeck scatterplot map that plots all of the listings in the chosen state. The points' radii are chosen based
    on the price of the car, and the color is chosen based on the region it was posted in. They also have tooltips, which
    show more useful information about each listing as the user hovers over each point.

Credit for multi-page web-app structure:
    This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps)
    framework developed by Praneel Nihar.

"""
import streamlit as st
from multiapp import MultiApp
from apps import app1, app2

# use whole page width
st.set_page_config(layout="wide")

app = MultiApp()

# Add all your application here
app.add_app("Search for a Listing", app1.app)
app.add_app("Listings by Region", app2.app)

# The main app
app.run()
