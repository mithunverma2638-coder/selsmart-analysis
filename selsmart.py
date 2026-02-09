import streamlit as st # streamlit is a Python library for creating interactive web apps
import pandas as pd # pandas is a library for data manipulation and analysis
import numpy as np # numpy is a library for numerical computing
import datetime # datetime is a module for working with dates and times
from PIL import Image # PIL is a library for image processing
import plotly.express as px # plotly is a library for creating interactive visualizations
import plotly.graph_objects as go # plotly.graph_objects is a module for creating complex visualizations
from pathlib import Path

df = pd.read_excel(r"MIS Overview of Selsmart Current Pending.xlsx") # reading the data from an Excel file
df_status = df['Order Status'].value_counts().reset_index() # creating an aggregated dataframe with order status counts
df_status.columns = ['Order Status', 'Count'] # renaming columns for the chart
st.set_page_config(layout="wide") # setting the page layout to wide
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True) # adding custom CSS to the app
image = Image.open(r"C:\Users\Mithun Verma\OneDrive - ATTERO RECYCLING PRIVATE LIMITED\Desktop\Project 3\Streamlit\selsmart png.jpg") # opening an image file

col1, col2 = st.columns([0.1,0.9]) # creating two columns with different widths
with col1: # adding content to the first column
    st.image(image, width=100) # displaying the image in the first column

html_title = """
    <style>
    .title_test {
    font-weight:bold;
    padding: 5px;
    border-radius:6px}
    </style>
    <center><h1 class= "title_test">Selsmart Analysis</h1></center>"""
with col2: # adding content to the second column
    st.markdown(html_title, unsafe_allow_html=True) # displaying the title in the second column 

# adding a filter for order status
st.sidebar.header("Filters")
all_status = df_status['Order Status'].unique().tolist()
selected_status = st.sidebar.multiselect("Select Order Status", options=all_status, default=all_status) # multiselect filter for order status
df_filtered = df_status[df_status['Order Status'].isin(selected_status)] # filtering the dataframe based on selected status

col3, col4, col5 = st.columns([0.1,0.45,0.45]) # creating three columns with different widths
with col3: # adding content to the third column
    box_date = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")) # getting the current date and time
    st.write(f"Last updated by: \n {box_date}") # displaying the last updated date in the third column

with col4: # adding content to the fourth column
    fig = px.bar(df_filtered, x="Order Status", y="Count", labels={"Order Status": "Order Status", "Count": "Count"}, 
                title="Distribution of Order Status", hover_data=["Count"], template="plotly_white", height=500) # creating a bar chart using plotly
    st.plotly_chart(fig, use_container_width=True) # displaying the bar chart in the fourth column

with col5: # adding content to the fifth column
    fig = px.pie(df_filtered, names="Order Status", values="Count", 
                title="Proportion of Order Status", 
                color_discrete_sequence=px.colors.sequential.RdBu) # creating a pie chart using plotly
    st.plotly_chart(fig, use_container_width=True) # displaying the pie chart in the fifth column

st.markdown("""---""") # adding a horizontal line separator

# creating a download button for the data file
with st.container(): # using a container to hold the download button
    st.subheader("Download the data") # adding a subheader for the download section
    st.markdown("Click the button below to download the data used in this analysis.", unsafe_allow_html=True) # adding a description for the download button
    st.download_button(label="Download data", 
                        data=df.to_csv(index=False).encode("utf-8"), # converting the dataframe to CSV format
                        file_name="selsmart_data.csv", # specifying the file name for the downloaded file
                        mime="text/csv", # specifying the MIME type for CSV files
                        )
_, view1, dwn1, view2, dwn2, _ = st.columns([0.05,0.20,0.20,0.20,0.20,0.15]) # creating columns for the view and download buttons   
with view1:
    expander = st.expander("Total Orders") # creating an expander to view the data
    data = df[["Order No", "Order Status", "State", "Order Date","Status Date","Warehouse Location"]] # selecting specific columns to display in the expander
    expander.write(data) # displaying the selected data in the expander

# create two columns for the additional charts
col6, col7 = st.columns([0.5, 0.5])

with col6:
    fig1 = px.histogram(df, x="Order Date", color="Order Status", title="Trend of Orders Over Time", template="plotly_white") # creating a histogram to show the trend of orders over time
    st.plotly_chart(fig1, use_container_width=True) # displaying the histogram in the sixth column

with col7:
    state_counts = df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig2 = px.bar(state_counts, x="State", y="Count", title="Distribution of Orders by State", template="plotly_white") # creating a bar chart to show the distribution of orders by state
    st.plotly_chart(fig2, use_container_width=True) # displaying the bar chart in the seventh column    