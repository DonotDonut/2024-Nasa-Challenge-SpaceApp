import streamlit as st
import subprocess  # Import subprocess module
import matplotlib.pyplot as plt
import numpy as np
from astroquery.gaia import Gaia
import pandas as pd
import time
from astroquery.exceptions import RemoteServiceError
from streamlit_drawable_canvas import st_canvas
import io
from PIL import Image, ImageOps

# Page Configurations
st.set_page_config(layout="centered", page_icon="📺", page_title="Exoplanet Gallery")

# URLs for different planets
kepler_url = "https://eyes.nasa.gov/apps/exo/#/planet/Kepler-808_b"
hats_url = "https://eyes.nasa.gov/apps/exo/#/planet/HATS-74_A_b"
kelt_url = "https://eyes.nasa.gov/apps/exo/#/planet/KELT-21_b"

# CSS for Styling Bubbles with Images
def set_css():
    st.markdown("""
        <style>            
            .bubble-container {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                margin: 20px auto;
                color: black;
            }
            .bubble {
                display: inline-block;
                width: 150px;
                height: 150px;
                border-radius: 75px;
                background: #007BFF;
                margin: 20px;
                transition: transform 0.3s;
                overflow: hidden;
                cursor: pointer;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                color: black;
            }
            .bubble img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: 75px;
                color: black;
            }
            .bubble:hover {
                transform: scale(1.1);
            }
                
            .main, .stApp {
                background-color: white;
                color: black;
            }
            
            .stApp h1, .stApp h2 {
                color: black;
            }
                
        </style>
    """, unsafe_allow_html=True)

# Function to show 360° view for exoplanets
def show_360_view(exoplanet_name, iframe_link):
    st.title(f"{exoplanet_name} - 360° View")
    st.markdown(f'<iframe src="{iframe_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'main'
    with col2:
        if st.button("Landing View"):
            st.session_state.page = 'landing'
    with col3:
        if st.button("🔭 Telescope View"):
            st.session_state.page = 'telescope'

# Choosinh a star
def main_content():
    st.title("Stars")

    # Create a bubble container with clickable bubbles
    cols = st.columns(3)
    starNames = [
        "Proxima Centra",
        "Ross 128",
        "Wolf 1067",
        "Kapteyn's Star", 
        "K2-18", 
        "Tau Centauri", 
        "GJ 667C", 
        "Gliese 832", 
        "YZ Centauri", 
        "HD 219134"
    ]

    for i in range(0, 9, 3): # Indexing error so I'm only including 9 (Will fix in the future)
        with cols[0]:  
            if st.button(starNames[i]):
                None
                #st.session_state.page = starNames[i]
        with cols[1]: 
            if st.button(starNames[i+1]):
                if starNames[i+1] == "K2-18":
                    st.session_state.page = starNames[i+1]
                else:
                    None
        with cols[2]: 
            if st.button(starNames[i+2]):
                None
                #st.session_state.page = starNames[i+2]

    ## Check for specific button action
    #if st.button("K2-18"):
    #    st.session_state.page = 'K2-18'
    


# Main content with buttons for different exoplanets
def exoplanent_content():
    st.title("Explore Exoplanets")

    # Create a bubble container with clickable bubbles
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Kepler-808 b"):
            st.session_state.page = 'Kepler-808_b'

    with col2:
        if st.button("HATS-74 A b"):
            st.session_state.page = 'HATS-74_A_b'
    
    with col3:
        if st.button("KELT-21 b"):
            st.session_state.page = 'KELT-21_b'

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


# CSS for Styling
def set_cssLanding():
    st.markdown("""
        <style>
            body {
                background-color: #f5f5f5;
            }
            h1 {
                text-align: center;
                color: #333;
            }
        </style>
    """, unsafe_allow_html=True)

# Function to display the 360° view for the exoplanet
def show_360_LandView(exoplanet_name, iframe_link):
    st.title(f"{exoplanet_name} - 360° View")
    st.markdown(f'<iframe src="{iframe_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)


# Main App Logic
if 'page' not in st.session_state:
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    set_css()
    main_content()

elif st.session_state.page == 'K2-18':
    set_css()
    exoplanent_content()


# Show the 360° view for each planet based on user choice
elif st.session_state.page == 'Kepler-808_b':
    set_css()
    show_360_view('Kepler-808 b', kepler_url)

elif st.session_state.page == 'HATS-74_A_b':
    set_css()
    show_360_view('HATS-74 A b', hats_url)

elif st.session_state.page == 'KELT-21_b':
    set_css()
    show_360_view('KELT-21 b', kelt_url)

# Show telescope view when the user clicks the "Telescope View" button
elif st.session_state.page == 'telescope':
    set_css()
    show_telescope_view()



# Showing Landing View
elif st.session_state.page == 'landing':
    set_cssLanding()
    show_360_view('Tau Ceti E', 'https://skybox.blockadelabs.com/e/7ccd18d63ee7d666a128776f4f36f605')  # Show the 360° view of Tau Ceti E




