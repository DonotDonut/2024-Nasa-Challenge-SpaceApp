import streamlit as st
import pandas as pd
import requests
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import plotly.express as px

# Query NASA Exoplanet Archive using ADQL
def query_nasa_exoplanet_data():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    query = """
    SELECT pl_name, ra, dec
    FROM ps
    WHERE ra IS NOT NULL AND dec IS NOT NULL
    """
    
    response = requests.post(url, data={'query': query, 'format': 'json'})

    # Check if the response was successful
    if response.status_code != 200:
        st.error(f"Error: Unable to fetch data from NASA Exoplanet Archive (Status code: {response.status_code})")
        st.write(response.content)  # Print response content for debugging
        return pd.DataFrame()  # Return an empty DataFrame on error

    exoplanet_data = pd.DataFrame(response.json())

    # Check if the DataFrame has data
    if exoplanet_data.empty:
        st.error("No data returned from the NASA Exoplanet Archive.")
    else:
        st.write("Columns in the DataFrame:", exoplanet_data.columns.tolist())
        st.write(exoplanet_data.head())  # Display the first few rows of the DataFrame

    return exoplanet_data

# Set up Streamlit app
st.title("NASA Exoplanet Archive Data Query")

# Query exoplanet data and display it
exoplanet_data = query_nasa_exoplanet_data()

if not exoplanet_data.empty:
    st.write(exoplanet_data)

    # Convert RA and DEC to pixel coordinates for plotting
    coords = SkyCoord(exoplanet_data['ra'], exoplanet_data['dec'], unit=(u.deg, u.deg))
    exoplanet_data['x'] = coords.ra.wrap_at(180 * u.deg)
    exoplanet_data['y'] = coords.dec

    # Create plotly scatter plot without gridlines
    fig = px.scatter(
        exoplanet_data,
        x='x',
        y='y',
        hover_name='pl_name',
        title='Exoplanets in the Milky Way'
    )

    '''# Update layout to include the Milky Way background image
    fig.add_layout_image(
        dict(
            source="milky_way_background.jpg",
            x=-np.pi,
            y=-np.pi / 2,
            xref="x",
            yref="y",
            sizex=2 * np.pi,
            sizey=np.pi,
            sizing="contain",
            opacity=0.5,
            layer="below"
        )
    )'''

    # Hide grid lines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')  # Set background color to transparent

    # Show the plot in Streamlit
    st.plotly_chart(fig)
