import streamlit as st
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from astroquery.gaia import Gaia
from astroquery.exceptions import RemoteServiceError
from streamlit_drawable_canvas import st_canvas
import io
from PIL import Image, ImageOps

st.page_link("homepage.py", label="Home", icon="🏠")
st.page_link("pages/Exoplanet_3D.py", label="Exoplanet_3D", icon="1️⃣")

# Dictionary to hold star data
star_data = {
    "K2-18": {
        "exoplanets": {
            "K2-18 b": {
                "orbit_url": "https://eyes.nasa.gov/apps/exo/#/planet/K2-18_b",
                "landing_url": "https://skybox.blockadelabs.com/e/5da2b296403e5e4802d1fe2cebc0262c"
            },
            "K2-18 c": {
                "orbit_url": "https://eyes.nasa.gov/apps/exo/#/planet/K2-18_c",
                "landing_url": "https://skybox.blockadelabs.com/e/faf4efe95b76063c14095b5fcc72ec2c"
            }
        }
    },
    "Kelt 21": {
        "exoplanets": {
            "KELT-21 b": {
                "orbit_url": "https://eyes.nasa.gov/apps/exo/#/planet/KELT-21_b",
                "landing_url": "https://skybox.blockadelabs.com/e/7ccd18d63ee7d666a128776f4f36f605"
            }
        }
    }
    # Add more stars and their exoplanets as needed
}

# CSS for Styling
def set_css():
    st.markdown("""
        <style>
            .main, .stApp {
                background-color: #1a1a1a; /* Darker background */
                color: white; /* White text */
            }
            
            /* Navigating (Regular) Button Styling */
            div.stButton > button {
                background-color: brown; /* Button background */
                color: white; /* Button text */
                border: none; /* No border */
                padding: 0.5em 1em; /* Padding */
                font-size: 16px; /* Font size */
                border-radius: 10px; /* Rounded corners */
                cursor: pointer; /* Pointer cursor */
            }
            
            div.stButton > button:hover {
                background-color: #8B4513; /* Darker brown on hover */
            }
            
            /* Download Button Styling */
            div.stDownloadButton > button {
                background-color: brown; /* Button background */
                color: white; /* Button text */
                border: none; /* No border */
                padding: 0.5em 1em; /* Padding */
                font-size: 16px; /* Font size */
                border-radius: 10px; /* Rounded corners */
                cursor: pointer; /* Pointer cursor */
            }
            
            div.stDownloadButton:hover {
                background-color: #8B4513; /* Darker brown on hover */
            }
            
            
            /* Title Styling */
             h1, h2, h3, h4, h5, h6 {
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# Main content to select stars
def main_content():
    st.title("Stars")
    for star_name in star_data.keys():
        if st.button(star_name):
            st.session_state.page = "exoplanet"
            st.session_state.selected_star = star_name

# Content for selecting exoplanets
def exoplanet_content():
    selected_star = st.session_state.selected_star
    st.title(f"Explore Exoplanets in {selected_star}")

    exoplanets = star_data[selected_star]["exoplanets"]
    for exoplanet_name, urls in exoplanets.items():
        if st.button(exoplanet_name):
            st.session_state.page = "360_view"
            st.session_state.selected_exoplanet = exoplanet_name
            st.session_state.selected_urls = urls

    if st.button("🔙 Go Back"):
        st.session_state.page = 'main'

# Showing the Planets Orbit POV Page
def show_360_view():
    exoplanet_name = st.session_state.selected_exoplanet
    urls = st.session_state.selected_urls
    st.title(f"{exoplanet_name} - 360° View")

    orbit_link = urls['orbit_url']
    landing_link = urls['landing_url']

    st.markdown(f'<iframe src="{orbit_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📍 Landing View"):
            st.markdown(f'<iframe src="{landing_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔭 Telescope View"):
            st.session_state.page = 'telescope'
    
    with col3:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'exoplanet'
   
       
       
            

# Function to display telescope/star chart view
def show_telescope_view():
    st.title("Interactive Star Chart with Free Drawing")

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
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        return fig

    # Function to resize drawn image to match the size of the star chart
    def resize_image(image, size):
        return ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)

    # Step 1: Query real star data from Gaia
    if "stars" not in st.session_state:
        stars = query_gaia_data(limit=100)  # Query 100 stars
        st.session_state.stars = stars
        st.session_state.star_chart_image = None  # Initialize star chart image
        st.session_state.drawn_image = None  # Initialize drawn image
        st.session_state.canvas_result = None  # Initialize canvas result

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

        # Step 3: Create a drawing canvas on top of the star chart image
        st.write("Draw on the star chart below:")

        # Define the canvas where users can draw freely
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Orange fill for objects
            stroke_width=2,
            stroke_color="red",  # Red stroke for drawing
            background_image=st.session_state.star_chart_image,  # Use the star chart image as the background
            update_streamlit=True,
            height=700,
            width=700,
            drawing_mode="freedraw",
            key="canvas",
        )

        # Save the drawn image in the session state
        if canvas_result.image_data is not None:
            drawn_image = Image.fromarray(canvas_result.image_data.astype("uint8"), mode="RGBA")
            st.session_state.drawn_image = drawn_image

        # Step 4: Merge drawing and star chart (if any)
        if st.session_state.drawn_image is not None:
            # Resize the drawn image to match the size of the star chart
            resized_drawn_image = resize_image(st.session_state.drawn_image, st.session_state.star_chart_image.size)

            # Merge the two images
            final_image = Image.alpha_composite(st.session_state.star_chart_image.convert("RGBA"), resized_drawn_image.convert("RGBA"))

            # Step 5: Convert the final image to a downloadable format
            buf = io.BytesIO()
            final_image.save(buf, format="PNG")
            buf.seek(0)

            # Step 6: Add a download button for the final image
            st.download_button(
                label="Download Final Star Chart",
                data=buf,
                file_name="final_star_chart.png",
                mime="image/png"
            )
    
    # Go Back button to return to star selection
    st.write("")  # Add spacing

    # format for go back button 
    col1, col2, col3 = st.columns(3)
    
    # go back button 
    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'main'


# Main App Logic
if 'page' not in st.session_state:
    st.session_state.page = 'main'

set_css()  # Apply CSS styles
if st.session_state.page == 'main':
    main_content()
elif st.session_state.page == 'exoplanet':
    exoplanet_content()
elif st.session_state.page == '360_view':
    show_360_view()
elif st.session_state.page == 'telescope':
    show_telescope_view()
