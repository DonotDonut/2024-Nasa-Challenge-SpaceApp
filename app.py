# Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from astroquery.gaia import Gaia

# Function to query Gaia data for galaxies and their distance (parallax)
def query_galaxies():
    query = """
    SELECT ra, dec, parallax, source_id, phot_g_mean_mag
    FROM gaiadr3.gaia_source
    WHERE classprob_dsc_combmod_galaxy > 0.8 AND parallax IS NOT NULL
    """
    job = Gaia.launch_job(query)
    galaxy_data = job.get_results().to_pandas()

    # Calculate the distance in parsecs from parallax
    galaxy_data['distance'] = 1 / galaxy_data['parallax']
    
    # Filter out negative distances
    galaxy_data = galaxy_data[galaxy_data['distance'] > 0]
    
    # Create a name column, defaulting to "Unknown Galaxy" if source_id is not found
    galaxy_data['name'] = "Unknown Galaxy"
    if 'source_id' in galaxy_data.columns:
        galaxy_data['name'] = "Galaxy " + galaxy_data['source_id'].astype(str)

    return galaxy_data

# Function to convert RA, Dec, and distance to Cartesian coordinates
def spherical_to_cartesian(ra, dec, distance):
    # Convert RA and Dec from degrees to radians
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    # Convert spherical (RA, Dec, distance) to Cartesian coordinates (x, y, z)
    x = distance * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance * np.sin(dec_rad)

    return x, y, z

# Function to plot galaxies in 3D with observer at the center (0, 0, 0)
def plot_galaxies(galaxy_data, color_scale_min, color_scale_max, dot_size):
    # Convert the galaxy RA, Dec, and distances into Cartesian coordinates
    galaxy_data["x"], galaxy_data["y"], galaxy_data["z"] = zip(*galaxy_data.apply(
        lambda row: spherical_to_cartesian(row["ra"], row["dec"], row["distance"]), axis=1
    ))

    # Prepare hover text for the plot
    hover_text = []
    for index, row in galaxy_data.iterrows():
        hover_text.append(f"{row['name']}<br>RA: {row['ra']}<br>Dec: {row['dec']}<br>Distance: {row['distance']:.2f} parsecs<br>Magnitude: {row['phot_g_mean_mag']}")

    # Create a 3D scatter plot with the observer (Earth or exoplanet) at the center
    fig = go.Figure(data=[go.Scatter3d(
        x=galaxy_data["x"],
        y=galaxy_data["y"],
        z=galaxy_data["z"],
        mode='markers',
        marker=dict(
            size=dot_size, 
            color=np.where(
                (galaxy_data['distance'] >= color_scale_min) & (galaxy_data['distance'] <= color_scale_max),
                galaxy_data['distance'],  # Use actual distance for color within the selected range
                np.nan  # Set non-selected distances to NaN
            ),
            colorscale='Magma',  # Default color scale
            cmin=color_scale_min,  # Minimum value for color scale
            cmax=color_scale_max,  # Maximum value for color scale
            colorbar=dict(title='Distance (parsecs)', titleside='right'),
            opacity=0.8
        ),
        text=hover_text,  # Use hover text created earlier
        hoverinfo='text',
        name='Galaxies'
    )])

    # Set the plot to center around (0, 0, 0) and enable rotation around this point
    fig.update_layout(scene=dict(
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-200, 200]),  # Set fixed axis range
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-200, 200]),  # Set fixed axis range
        zaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-200, 200]),  # Set fixed axis range
        aspectmode='cube',  # Ensures equal scaling along all axes
        camera=dict(
            eye=dict(x=0, y=-2, z=2),  # Set initial view closer to the center
            center=dict(x=0, y=0, z=0),  # Keep the center at (0, 0, 0)
        )
    ))

    return fig

# Streamlit app
st.title("Galaxies Viewer in Astronomical Coordinates")

# Query Gaia data for galaxies and their distances
galaxy_data = query_galaxies()

# Slider for color scale range
color_scale_min, color_scale_max = st.slider(
    'Select Distance Range for Color Scale',
    min_value=float(galaxy_data['distance'].min()),
    max_value=float(galaxy_data['distance'].max()),
    value=(float(galaxy_data['distance'].min()), float(galaxy_data['distance'].max()))
)

# Slider for dot size
dot_size = st.slider('Select Dot Size', min_value=1, max_value=20, value=5)

# Plot the galaxies in 3D with the observer at the center
fig = plot_galaxies(galaxy_data, color_scale_min, color_scale_max, dot_size)

# Display the 3D plot
st.plotly_chart(fig, use_container_width=True)

st.write("The plot is centered around the observer, and galaxies are positioned based on RA, Dec, and distance. The color gradient indicates the actual distance of the galaxies.")
