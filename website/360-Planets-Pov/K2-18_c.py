import streamlit as st

# Page Configurations
#st.set_page_config(layout="centered", page_icon="📺", page_title="Exoplanet Gallery")

# CSS for Styling
def set_css():
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
def show_360_view(exoplanet_name, iframe_link):
    st.title(f"{exoplanet_name} - 360° View")
    st.markdown(f'<iframe src="{iframe_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)

# Main App Logic
set_css()  # Set CSS styles
show_360_view('K2-18 c', 'https://skybox.blockadelabs.com/e/faf4efe95b76063c14095b5fcc72ec2c')  # Show the 360° view of Tau Ceti E