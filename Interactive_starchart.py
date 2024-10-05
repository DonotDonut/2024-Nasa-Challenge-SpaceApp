import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from astroquery.gaia import Gaia
import pandas as pd
import time
from astroquery.exceptions import RemoteServiceError
from streamlit_drawable_canvas import st_canvas
import io
from PIL import Image

# Example fallback dataset if Gaia query fails
def fallback_star_data():
    return pd.DataFrame({
        'ra': np.random.uniform(0, 360, 100),  # Random RA values
        'dec': np.random.uniform(-90, 90, 100),  # Random Dec values
        'phot_g_mean_mag': np.random.uniform(1, 10, 100)  # Random brightness
    })

# Query Gaia Data with fallback
def query_gaia_data(limit=100, retries=3, delay=5):
    for attempt in range(retries):
        try:
            job = Gaia.launch_job_async(
                f"SELECT ra, dec, phot_g_mean_mag "
                f"FROM gaiadr3.gaia_source "
                f"WHERE phot_g_mean_mag < 10 LIMIT {limit}"
            )
            stars = job.get_results().to_pandas()
            return stars
        except RemoteServiceError as e:
            st.error(f"Error querying Gaia: {str(e)}. Retrying in {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            break
    
    # If query fails, return fallback data
    st.warning("Unable to query Gaia data. Using fallback star data.")
    return fallback_star_data()

# Plot the star chart using polar projection
def plot_star_chart(stars):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='polar')

    # Convert RA to radians and Dec to radius (Stereographic projection)
    ra_radians = np.deg2rad(stars["ra"])  # Convert RA to radians
    dec_radius = 90 - np.abs(stars["dec"])  # Declination to radius in polar plot

    # Normalize star sizes based on brightness
    star_sizes = np.clip(20 / (stars["phot_g_mean_mag"] + 1), 10, 100)  # Normalize size to avoid extreme values
    star_colors = plt.cm.viridis(1 - (stars["phot_g_mean_mag"] / 10))  # Color based on magnitude

    # Scatter plot for stars
    ax.scatter(ra_radians, dec_radius, s=star_sizes, c=star_colors, alpha=0.8)

    # Customize the star chart appearance
    ax.set_facecolor('black')  # Black background for space effect
    ax.set_theta_zero_location('S')  # 0 degrees RA at the bottom (South)
    ax.set_ylim(0, 90)  # Limit to hemisphere (Declination range)
    
    # Hide axis labels and grids for a clean look
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    return fig

# Streamlit App
st.title("Interactive Star Chart with Free Drawing")

# Step 1: Query real star data from Gaia
st.write("Fetching star data from the Gaia catalog...")

# Only query data and plot the chart once
if "stars" not in st.session_state:
    stars = query_gaia_data(limit=100)  # Query 100 stars
    st.session_state.stars = stars
    st.session_state.star_chart_image = None  # Initialize star chart image

if st.session_state.stars is not None and not st.session_state.stars.empty:
    st.write("Star data fetched successfully.")
    
    # Step 2: Plot the circular star chart only once
    if st.session_state.star_chart_image is None:
        st.write("Rendering star chart...")
        
        # Create a star chart image
        fig = plot_star_chart(st.session_state.stars)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0, transparent=True)
        buf.seek(0)
        
        # Store the star chart image in session state
        st.session_state.star_chart_image = Image.open(buf)

    # Display the star chart image
    st.image(st.session_state.star_chart_image, caption="Star Chart", use_column_width=True)

    # Step 3: Create a drawing canvas on top of the star chart image
    st.write("Draw on the star chart below:")

    # Initialize session state for drawing
    if "drawn_image" not in st.session_state:
        st.session_state.drawn_image = None

    # Define the canvas where users can draw freely
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Orange fill for objects
        stroke_width=2,
        stroke_color="#FFFFFF",  # White strokes for drawing
        background_color="rgba(0, 0, 0, 0)",  # Transparent background to see star chart
        height=600,
        width=600,
        drawing_mode="freedraw",  # Free drawing mode
        key="canvas",
        background_image=st.session_state.star_chart_image  # Set the star chart image as the background
    )

    # Update session state with the drawn image if present
    if canvas_result.image_data is not None:
        st.session_state.drawn_image = Image.fromarray(canvas_result.image_data.astype(np.uint8))

    # Show the drawn image if it exists
    if st.session_state.drawn_image is not None:
        st.image(st.session_state.drawn_image, caption="Your drawing on the star chart", use_column_width=True)

    # Provide an erase button to clear the drawing
    if st.button("Erase Drawing"):
        st.session_state.drawn_image = None  # Clear the drawing

        # Clear the canvas by redrawing the chart with the same background
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Orange fill for objects
            stroke_width=2,
            stroke_color="#FFFFFF",  # White strokes for drawing
            background_color="rgba(0, 0, 0, 0)",  # Transparent background to see star chart
            height=600,
            width=600,
            drawing_mode="freedraw",  # Free drawing mode
            key="canvas",
            background_image=st.session_state.star_chart_image  # Set the star chart image as the background
        )

    # Combine the star chart and the drawing if it exists
    if st.session_state.drawn_image is not None:
        final_image = Image.alpha_composite(st.session_state.star_chart_image.convert("RGBA"), st.session_state.drawn_image.convert("RGBA"))

        # Save the final image to a BytesIO object for downloading
        final_buf = io.BytesIO()
        final_image.save(final_buf, format="PNG")
        final_buf.seek(0)

        # Provide a download link for the final image
        st.download_button(
            label="Download Your Star Chart with Constellations",
            data=final_buf,
            file_name="star_chart_with_constellations.png",
            mime="image/png"
        )

else:
    st.warning("No star data to display.")
