"""
Name:       Anthony Medugno
CS230 - SN1
Data:       cl_used_cars_7000_sample.csv
URL:        Link to your web application online (see extra credit)

Description: (a few sentences about your program and the queries and charts)

This program contains 2 different functions (i.e. queries).
1. Allows the user to filter data using Streamlit UI controls and Pandas dataframes.
In this case the user may be a customer looking to purchase a used car based on some preferences.
The output of this query will be displayed in a Streamlit UI table.

"""
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd

# import dataset
datafile = "cl_used_cars_7000_sample.csv"
df = pd.read_csv(datafile, header=0)

# search data based on params
def searchData(df, carPriceRange, carCondition, carManufac, carSizesPickedList, carTypesPickedList):
    # filter dataframe here
    # Price Range
    dfSearch = df[df['price'] >= carPriceRange[0]]
    dfSearch = dfSearch[dfSearch['price'] <= carPriceRange[1]]

    # Condition
    dfSearch = dfSearch[dfSearch['condition']==carCondition.lower()]

    # Manufac
    dfSearch = dfSearch[dfSearch['manufacturer']==carManufac.lower()]

    # Size
    carSizesPickedList = [x.lower() for x in carSizesPickedList]
    dfSearch = dfSearch[dfSearch['size'].isin(carSizesPickedList)]

    # Type
    carTypesPickedList = [x.lower() for x in carTypesPickedList]
    dfSearch = dfSearch[dfSearch['type'].isin(carTypesPickedList)]

    return dfSearch


# 1st app page -- this is like a main() function
def app():

    # make list of options for each UI control requiring a list of options
    seriesList = [series.dropna().str.title().drop_duplicates().tolist()
                  for series in [df['manufacturer'], df['condition'], df['size'], df['type']]]


    # ** SIDEBAR SECTION **

    # input for search
    st.sidebar.header('Filters: ')
    st.sidebar.write('Use the following filters to search through the dataset for used cars.')
    carPriceRange = st.sidebar.slider("Price Range: ",0,int(df['price'].max()),(0,100000),format='$%d')
    carCondition = st.sidebar.radio("Condition: ", seriesList[1])
    carManufac = st.sidebar.selectbox("Manufacturer: ", seriesList[0])

    #carSize = st.sidebar.slider("Size: ", seriesList[2])

    # Checkboxes for carSize option
    st.sidebar.write("Vehicle size: ")
    sizesCheckboxes = [st.sidebar.checkbox(label, key=label) for label in seriesList[2]]
    carSizesPickedList = [label for label, checked in zip(seriesList[2], sizesCheckboxes) if checked]

    # next option
    carTypesPickedList = st.sidebar.multiselect("Vehicle type: ", seriesList[3])

    # ** MAIN PAGE BODY SECTION **

    # Filter the Dataset
    filteredDf = searchData(df, carPriceRange, carCondition, carManufac, carSizesPickedList, carTypesPickedList)

    st.title('Search for a Car:')
    st.header(f'We found {filteredDf["id"].count()} matching listings!')


    st.subheader('Table View:')
    # select which columns to include in results table
    # default columns to show
    columnsPickedList = st.multiselect("Pick your own columns to show: ",df.columns.tolist()[2:],
                        default=['state','region','year','manufacturer',
                                 'model','cylinders','odometer','paint_color','price','posting_date'])

    # display DF in interactive table
    st.write(filteredDf[columnsPickedList])

    st.markdown('##') #for whitespace

    # ** DISPLAY DATA AS HTML TILES **
    st.subheader('Catalog View:')
    # Need stylesheet and starting flex container div
    htmlContainer="""
    <style>
    .flip-card {
      background-color: transparent;
      width: 363px;
      height: 300px;
      perspective: 1000px;
    }
    
    .flip-card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s;
      transform-style: preserve-3d;
      box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    
    .flip-card:hover .flip-card-inner {
      transform: rotateY(180deg);
    }
    
    .flip-card-front, .flip-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border: 3px solid #3498db;
      border-radius: 5px;
    }
    
    .flip-card-front {
      background-color: #fff;
      color: #2c3e50;
      font-size: 20px;
    }
    
    .flip-card-back {
      background-color: whitesmoke;
      color: #2c3e50;
      transform: rotateY(180deg);
    }
    
    #flexRow>.flexChild {
        margin: 20px 30px;
    }
    
    .cardButton {
        background-color: #1c87c9;
        border: none;
        color: white;
        padding: 10px 17px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 20px;
        margin: 4px 2px;
        cursor: pointer;
    }
    
    </style>
    
    <div id="flexRow" style="display: flex; flex-wrap: wrap;">
    """

    htmlFlexChildren=""


    for row in filteredDf[['url', 'image_url','manufacturer','model', 'year', 'price']].dropna().itertuples():
        htmlFlexChild=f"""
        <div class="flexChild">
            <div class="flip-card">
              <div class="flip-card-inner">
                <div class="flip-card-front">
                  <img src="{row.image_url}" onerror="this.onerror=null;this.src='https://www.kindpng.com/picc/m/210-2102696_car-icon-blue-warren-street-tube-station-hd.png';" style="width:363px;height:300px;">
                </div>
                <div class="flip-card-back">
                  <h2>{row.year:.0f} {row.manufacturer.title()}</h2>
                  <h2>{row.model.title()}</h2>
                  <br> 
                  <h3>Price: ${row.price:,.2f}</h3>
                  <br> 
                  <a class="cardButton" style="color: white; font-weight: bold; text-decoration: none;" href="{row.url}" target="_blank">Buy Here</a>
                </div>
              </div>
            </div>
        </div>
        """
        htmlFlexChildren+=htmlFlexChild
    # Display html markup
    components.html(htmlContainer + htmlFlexChildren + "</div>", height=9000, scrolling=True)
