import streamlit as st


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
show_360_view('Kelt-21 b', 'https://skybox.blockadelabs.com/e/7ccd18d63ee7d666a128776f4f36f605')  # Show the 360° view of Tau Ceti E