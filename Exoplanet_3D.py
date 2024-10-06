import streamlit as st

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
            }
            .bubble img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: 75px;
            }
            .bubble:hover {
                transform: scale(1.1);
            }
        </style>
    """, unsafe_allow_html=True)

# Function to show 360° view for exoplanets
def show_360_view(exoplanet_name, iframe_link):
    st.title(f"{exoplanet_name} - 360° View")
    st.markdown(f'<iframe src="{iframe_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Go Back"):
            st.session_state.page = 'main'
    with col2:
        if st.button("🔭 Telescope View"):
            st.write(f"Telescope view of {exoplanet_name} is coming soon!")

# Main content with buttons for different exoplanets
def main_content():
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

# Main App Logic
if 'page' not in st.session_state:
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    set_css()
    main_content()

# Show the 360° view for each planet based on user choice
elif st.session_state.page == 'Kepler-808_b':
    show_360_view('Kepler-808 b', kepler_url)

elif st.session_state.page == 'HATS-74_A_b':
    show_360_view('HATS-74 A b', hats_url)

elif st.session_state.page == 'KELT-21_b':
    show_360_view('KELT-21 b', kelt_url)

