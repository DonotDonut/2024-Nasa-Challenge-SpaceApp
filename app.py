# Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from astroquery.gaia import Gaia
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

# Function to query Gaia data for stars/exoplanets and their distance (parallax)
def query_exoplanets():
    query = """
    SELECT ra, dec, parallax, source_id, phot_g_mean_mag
    FROM gaiadr3.gaia_source
    WHERE classprob_dsc_combmod_star > 0.8 AND parallax IS NOT NULL
    """
    job = Gaia.launch_job(query)
    exoplanet_data = job.get_results().to_pandas()

    # Convert parallax to distance in parsecs (parallax is in milliarcseconds)
    exoplanet_data['distance'] = 1000 / exoplanet_data['parallax']  # Convert to parsecs

    # Filter out nonsensical or negative distances
    exoplanet_data = exoplanet_data[exoplanet_data['distance'] > 0]

    # Create a name column for labeling the stars
    exoplanet_data['name'] = "Unknown Star"
    if 'source_id' in exoplanet_data.columns:
        exoplanet_data['name'] = "Star " + exoplanet_data['source_id'].astype(str)

    return exoplanet_data

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

# Function to plot exoplanets/stars in 3D with Earth centered at (0, 0, 0)
def plot_exoplanets(exoplanet_data, color_scale_min, color_scale_max, dot_size):
    # Convert RA, Dec, and distances into Cartesian coordinates
    exoplanet_data["x"], exoplanet_data["y"], exoplanet_data["z"] = zip(*exoplanet_data.apply(
        lambda row: spherical_to_cartesian(row["ra"], row["dec"], row["distance"]), axis=1
    ))

    # Prepare hover text for the plot
    hover_text = []
    for index, row in exoplanet_data.iterrows():
        hover_text.append(f"{row['name']}<br>RA: {row['ra']}<br>Dec: {row['dec']}<br>Distance: {row['distance']:.2f} parsecs<br>Magnitude: {row['phot_g_mean_mag']}")

    # Create a 3D scatter plot with Earth at the center (0, 0, 0)
    fig = go.Figure(data=[go.Scatter3d(
        x=exoplanet_data["x"],
        y=exoplanet_data["y"],
        z=exoplanet_data["z"],
        mode='markers',
        marker=dict(
            size=dot_size,
            color=exoplanet_data['distance'],  # Color based on distance
            colorscale='Viridis',  # Color scale for distance
            cmin=color_scale_min,  # Minimum value for color scale
            cmax=color_scale_max,  # Maximum value for color scale
            colorbar=dict(title='Distance (parsecs)', titleside='right'),
            opacity=0.8
        ),
        text=hover_text,  # Use hover text created earlier
        hoverinfo='text',
        name='Stars/Exoplanets'
    )])

    # Set the plot to center around Earth (0, 0, 0) and enable proper scaling
    fig.update_layout(scene=dict(
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-200, 200]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-200, 200]),
        zaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-200, 200]),
        aspectmode='cube',  # Ensures equal scaling along all axes
        camera=dict(
            eye=dict(x=0, y=-2, z=2),  # Set initial view closer to the center
            center=dict(x=0, y=0, z=0),  # Keep Earth at (0, 0, 0)
        )
    ))

    return fig

# Streamlit app
st.title("Exoplanets Viewer in Astronomical Coordinates")

# Query Gaia data for stars/exoplanets and their distances
exoplanet_data = query_exoplanets()

# Slider for color scale range
color_scale_min, color_scale_max = st.slider(
    'Select Distance Range for Color Scale',
    min_value=float(exoplanet_data['distance'].min()),
    max_value=float(exoplanet_data['distance'].max()),
    value=(float(exoplanet_data['distance'].min()), float(exoplanet_data['distance'].max()))
)

# Slider for dot size
dot_size = st.slider('Select Dot Size', min_value=1, max_value=20, value=5)

# Plot the stars/exoplanets in 3D with Earth at the center
fig = plot_exoplanets(exoplanet_data, color_scale_min, color_scale_max, dot_size)

# Display the 3D plot
st.plotly_chart(fig, use_container_width=True)

st.write("The plot is centered around Earth (0, 0, 0), and stars are positioned based on RA, Dec, and distance. The color gradient indicates the distance of the stars.")
