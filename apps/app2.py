"""
Name:       Anthony Medugno
CS230 - SN1
Data:       cl_used_cars_7000_sample.csv
URL:        Link to your web application online (see extra credit)

Description:
2. The only input on this page is to select a state on the sidebar. This page contains two different visualizations:
    A. a matplotlib bar graph that displays the most popular regions in a given state (using a dataframe that groups by
    region and counts the number of listings in each region.
    B. a PyDeck scatterplot map that plots all of the listings in the chosen state. The points' radii are chosen based
    on the price of the car, and the color is chosen based on the region it was posted in. They also have tooltips, which
    show more useful information about each listing as the user hovers over each point.

"""

import csv
import statistics
import datetime
import streamlit as st
import random
import numpy as np
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# import dataset
datafile = "cl_used_cars_7000_sample.csv"
df = pd.read_csv(datafile, header=0)


def buildDfsForMap(df, option):

    # get all listings in given state
    stateListings = df[df['state'] == option.lower()]

    # get list of regions in the state to iterate over them
    regionList = stateListings.region.unique()

    dfsList = []
    for region in regionList:
        # make a new dataframe for all the listings in each region with long, lat, price, and color values.
        # drop rows without values, reset the indexes and dont add the index column to the dataframe as a new column
        # and append it to the list to access later
        dfsList.append(df[['region','long','lat','year','manufacturer','model','price']][df['region'] == region].dropna().reset_index(drop=True))

    return dfsList, stateListings

def scattermap(dfsList):
    # plot dataframes on map

    # make list of layers to put layers into
    layersList = []

    # define list of colors to assign one to each layer
    cssColorsList = list(mcolors.CSS4_COLORS.keys())
    # convert hex colors to rgb
    #           *since hex colors aren't supported by the pyDeck layer get_fill_color attribute
    colorsList = [mcolors.to_rgba(c) for c in cssColorsList]
    # convert 0-1 scale to 0-255 scale
    colorsList = [[int(value*255) for value in color] for color in colorsList]

    # iterate over dataframes and put each one into a pyDeck layer
    # add each pyDeck layer to the layersList
    colorIncr = 10

    for df in dfsList:

        df['price_radius'] = df["price"].apply(lambda price: np.sqrt(price))

        # Write out legend items in the corresponding color
        # st.markdown(f'<font color=‘{cssColorsList[colorIncr]}’>{df.at[0,"region"].title()}</font>', unsafe_allow_html=True)

        layersList.append(
            # Define a layer to display on a map
            pdk.Layer(
                "ScatterplotLayer",
                df,
                pickable=True,
                opacity=0.8,
                stroked=True,
                filled=True,
                radius_scale=10,
                radius_min_pixels=1,
                radius_max_pixels=1000,
                line_width_min_pixels=1,
                get_position=['long', 'lat'],
                get_radius="price_radius",
                get_fill_color=colorsList[colorIncr],
                get_line_color=[0, 0, 0],
            )
        )
        colorIncr += 1

    view_state = pdk.ViewState(longitude=dfsList[0].at[0,'long'], latitude=dfsList[0].at[0,'lat'], zoom=4, bearing=0, pitch=0)
    tooltip = {
       "html": "<b>Region:</b> {region}"
            "<br/> <b>Manufacturer:</b> {manufacturer}"
            " <br/> <b>Model:</b> {model} "
            "<br/> <b>Year:</b> {year}"
            "<br/> <b>Price:</b> ${price}",
       "style": {
            "backgroundColor": "steelblue",
            "color": "white"
       }
    }
    # Render
    st.pydeck_chart(pdk.Deck(layers=[layersList], initial_view_state=view_state, tooltip=tooltip))

def barChart(stateOpt, colorOpt):

    # get all listings in given state
    stateListings = df[df['state'] == stateOpt.lower()]

    # groupby region and count frequency of regions
    series = stateListings.groupby(['region'])['region'].count().sort_values(ascending=False)

    # Chart 1: write a bar graph to the screen to visualize the frequencies
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_axes([0,0,1,1])
    ax.bar(series.index, series, color=colorOpt)
    ax.set_ylabel('Number of Listings')
    ax.set_xlabel('Region')
    ax.set_xticklabels(series.index, rotation=45, ha="right")
    return fig

# 2nd app page -- this is like a main() function
def app():

    # convert df to series of states, fix order and remove duplicates
    # convert df to list to use in selectbox
    statesList = df['state'].drop_duplicates().sort_values().str.upper().tolist()

    # Inputs for heatmap
    st.sidebar.header('Inputs: ')
    option = st.sidebar.selectbox('Select a State: ', statesList)
    colorPicked = st.sidebar.color_picker(f'Select color for bar graph: ','#f8536a')

    # Output Section
    st.title(f'Used Cars Listed in {option}:')
    st.markdown('##') #for whitespace
    # bar graph is displayed here -- constructed inside of buildFreqDf function

    # Build freq df
    dfsList, stateListings = buildDfsForMap(df, option)

    col1, col2, col3 = st.beta_columns((1,2,1))

    # Build / display bar chart
    fig = barChart(option, colorPicked)
    with col2:
        st.pyplot(fig)

    with col1, col3:
        st.markdown("##")

    # show heat map
    st.title(f'Map of {option} Listings:')
    st.write(f"""Each point on the map represents a listing for a used car; the radius is based on the price of the car, 
    and the color is chosen based on the region it was posted in. Hover over a point to reveal more useful info about the listing.""")
    st.markdown('##') #for whitespace
    scattermap(dfsList)




