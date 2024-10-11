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


# global variables  
#list of star names 
starNames = [
    "K2-18", "Kelt 21", "Ross 128",
    "Wolf 1067", "Kapteyn's Star", "Proxima Centra", 
    "Tau Centauri", "GJ 667C", "Gliese 832", 
    "YZ Centauri", "HD 219134"
    # Add more starts when needed 
]

#list of star names 
exoplanets = {
    "K2-18" : ["K2-18 b", "K2-18 c"],
    "Kelt 21" : ["KELT-21 b"],
     # Add more exoplants to their stars when needed 
}

# URLs for different planets outer orbit pov 
orbit_urls = {
    "kepler_url" : "https://eyes.nasa.gov/apps/exo/#/planet/K2-18_b" ,
    "hats_url" : "https://eyes.nasa.gov/apps/exo/#/planet/K2-18_c" , 
    "kelt_url" : "https://eyes.nasa.gov/apps/exo/#/planet/KELT-21_b"
}

# URL for different planets landing pov 
landing_urls = {
"K2-18 b" : "https://skybox.blockadelabs.com/e/5da2b296403e5e4802d1fe2cebc0262c" ,
"k2_18c_landing" : "https://skybox.blockadelabs.com/e/faf4efe95b76063c14095b5fcc72ec2c" ,
"kelt_21_landing" : "https://skybox.blockadelabs.com/e/7ccd18d63ee7d666a128776f4f36f605"
}


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
                background-color: #1a1a1a; /*Darker background*/
                color: white; /* White text for better contrast*/
            }
            
            .stApp h1, .stApp h2 {
                color: white; /* white headers*/
            }
                
            /* Button Styling ------------------------- */
            div.stButton > button {
                background-color: brown; / Brown background for buttons /
                color: white; / White text on the button /
                border: none; / Remove default borders /
                padding: 0.5em 1em;
                font-size: 16px;
                border-radius: 10px; / Rounded corners /
                cursor: pointer;
            }
            div.stButton > button:hover {
                background-color: #8B4513; / Darker brown on hover /
                color: white; / Keep white text on hover */
            }
            
            /* Download Button Styling ------------------------- */
            div.stDownloadButton > button {
                background-color: brown; / Brown background for buttons /
                color: white; / White text on the button /
                border: none; / Remove default borders /
                padding: 0.5em 1em;
                font-size: 16px;
                border-radius: 10px; / Rounded corners /
                cursor: pointer;
            }
            div.stDownloadButton  > button:hover {
                background-color: #8B4513; / Darker brown on hover /
                color: white; / Keep white text on hover */
            }
                
        </style>
    """, unsafe_allow_html=True)
    

# Choosing a star page -------------------------------------
def main_content():
    st.title("Stars")

    # Create a bubble container with clickable bubbles
    cols = st.columns(3)

    # Create rows of stars (3 stars per row)
    cols_per_row = 3
    for i in range(0, len(starNames), cols_per_row):
        cols = st.columns(cols_per_row)

        for idx, col in enumerate(cols):
            if i + idx < len(starNames):
                star_name = starNames[i + idx]
                with col:
                    if st.button(star_name):
                        # Check if the star has exoplanets
                        if star_name in exoplanets and exoplanets[star_name]:
                            st.session_state.page = "exoplanet"  # Navigate to the exoplanet page
                            st.session_state.selected_star = star_name  # Store the selected star
                        else:
                            st.write("None")  # Keep user on the main page 
   
    st.write("") # blank line 
    st.write("") # blank line 
    
    # Go back button 
    col1, _, _ = st.columns(3)
    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'main'

# end of Choosing star page ----------------------------------


# Selecting Exoplanet Page -----------------------------------
def exoplanent_content():
    # Ensure a star is selected
    if 'selected_star' in st.session_state and st.session_state.selected_star in starNames:
        selected_star = st.session_state.selected_star
        st.title(f"Explore Exoplanets in {selected_star}")

        # Check if the selected star has any exoplanets
        if selected_star in exoplanets:
            exoplanet_list = exoplanets[selected_star]

            # Create a bubble container with clickable bubbles
            cols_per_row = 3
            for i in range(0, len(exoplanet_list), cols_per_row):
                cols = st.columns(cols_per_row)

                for idx, col in enumerate(cols):
                    if i + idx < len(exoplanet_list):
                        exoplanet_name = exoplanet_list[i + idx]
                        with col:
                            if st.button(exoplanet_name):
                                st.session_state.page = "360_view"
                                st.session_state.selected_exoplanet = exoplanet_name  # Store the selected exoplanet
        else:
            st.write("No exoplanets found for this star.")  # Message if no exoplanets

    # Go Back button to return to star selection
    st.write("")  # Add spacing
    
    # Format for back button 
    col1, _, _ = st.columns(3)
    
    # Back button 
    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'main'

# End of Selecting Exoplanet Page -----------------------------------



# Showing the Planets Orbit POV Page -------------------------------------

# Function to show 360° view for exoplanets
def show_360_view():
    exoplanet_name = st.session_state.selected_exoplanet
    st.title(f"{exoplanet_name} - 360° View")
    
    # Determine the correct orbit URL based on the exoplanet name
    orbit_link = None
    if exoplanet_name == "K2-18 b":
        orbit_link = orbit_urls["kepler_url"]
    elif exoplanet_name == "K2-18 c":
        orbit_link = orbit_urls["hats_url"]
    elif exoplanet_name == "Kelt-21 b":
        orbit_link = orbit_urls["kelt_url"]

    # Render the 360° view iframe
    if orbit_link:
        st.markdown(f'<iframe src="{orbit_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)
    else:
        st.write("360° view is not available for this exoplanet.")

    # Layout for buttons
    col1, col2, col3 = st.columns(3)
    
    # Go Back button
    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'exoplanet'
    
    # Landing View button
    with col2:
        landing_url = landing_urls.get(exoplanet_name)
        if landing_url:
            if st.button("📍 Landing View"):
                st.markdown(f'<iframe src="{landing_url}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)
    
    # Telescope View button
    with col3:
        if st.button("🔭 Telescope View"):
            st.session_state.page = 'telescope'

            
# End of Showing the Planets Orbit POV Page -------------------------------------


# Telescope page ----------------------------------------------------

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
            
# End of Telescope page ----------------------------------------------------


# Landing page ----------------------------------------------------

# Function to display the 360° view for the exoplanet
def show_360_LandView(exoplanet_name, iframe_link):
    st.title(f"{exoplanet_name} - 360° View")

    # Use a centered container for the iframe
    st.markdown(f'''
        <div style="text-align: center;">
            <iframe src="{iframe_link}" width="700" height="700" style="border:0;" allow="fullscreen"></iframe>
        </div>
    ''', unsafe_allow_html=True)

    # Separate row for buttons (not affecting the iframe layout)
    st.write("")  # Add spacing for visual separation

    # Buttons in a row using columns
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'main'

    with col3:
        if st.button("🔭 Telescope View"):
            st.session_state.page = 'telescope'
    
# End of Landing page ----------------------------------------------------




# Main App Logic
# Check for session state 
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Navigation logic 
if st.session_state.page == 'main':
    set_css()
    main_content()  # Main page with stars

elif st.session_state.page == 'exoplanet':
    set_css()
    exoplanent_content()  # Show exoplanet options for the selected star

elif st.session_state.page == '360_view':
    set_css()
    show_360_view()  # Show the 360° view based on the selected exoplanet

elif st.session_state.page == 'telescope':
    set_css()
    show_telescope_view()  # Show telescope/star chart view


# Adjusted button action in main_content function
def main_content():
    st.title("Stars")
    # Create a bubble container with clickable bubbles
    cols = st.columns(3)

    # Create rows of stars (3 stars per row)
    cols_per_row = 3
    for i in range(0, len(starNames), cols_per_row):
        cols = st.columns(cols_per_row)

        for idx, col in enumerate(cols):
            if i + idx < len(starNames):
                star_name = starNames[i + idx]
                with col:
                    if st.button(star_name):
                        # Navigate to the exoplanet page when a star is selected
                        if star_name in exoplanets:
                            st.session_state.page = "exoplanet"  # Change to exoplanet page
                            st.session_state.selected_star = star_name  # Store selected star

    # Go back button
    col1, _, _ = st.columns(3)
    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'main'

