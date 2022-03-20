# Craigslist Used Car Data Visualization
For the final project of my *Intro to Python Programming* course at Bentley, each of us were told to use Streamlit to create a web app which visualizes a given dataset. You can find the dataset I used for this project <a href="https://www.kaggle.com/austinreese/craigslist-carstrucks-data" target="_blank">here</a>. Using this dataset, I constructed a two-page Streamlit app that contains 4 different visualizations.

  
<p style="text-indent: 0px">The first page allows the user to filter data using Streamlit UI controls and Pandas dataframes. In this case the user may be a customer looking to purchase a used car based on some preferences. You'll find the following visualizations on this page:</p>

1. a Streamlit UI table.
2. a Catalog section that makes use of custom HTML and CSS snippets to display a UI card for each listing.
    - The front of each card shows a preview image of the listing (or a default car icon if the preview image could not be found).
    - The back of each card lists the car's manufacturer, model, and price. It also provides a link to the original Craigslist listing for the car.

<p></p>
  
<p style="text-indent: 0px">The second page allows the user to filter the dataset by state. Once a state is selected, you'll see the following visualizations on this page:</p>

1. A *matplotlib* bar graph that displays the most popular regions in a given state (using a dataframe that groups by region and counts the number of listings in each region).
2. A *PyDeck* scatterplot map that plots all of the listings in the chosen state. The points' radii are chosen based on the price of the car, and the color is chosen based on the region it was posted in. They also have tooltips, which show more useful information about each listing as the user hovers over each point.
