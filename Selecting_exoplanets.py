import streamlit as st

# Page Configurations
st.set_page_config(layout="centered", page_icon="📺", page_title="Exoplanet Gallery")

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

# Main Page with Bubbles
def main_content():
    st.title("Explore Exoplanets")

    # Create a bubble container with clickable bubbles
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Tau Ceti E"):
            st.session_state.page = 'Tau_Ceti_E'
    
    with col2:
        if st.button("Tau Ceti F"):
            st.session_state.page = 'Tau_Ceti_F'
    
    with col3:
        if st.button("Exoplanet G"):
            st.session_state.page = 'Exoplanet_G'

# Exoplanet Detail Pages
def show_360_view(exoplanet_name, iframe_link):
    st.title(f"{exoplanet_name} - 360° View")
    st.markdown(f'<iframe src="{iframe_link}" width=700 height=700 style="border:0;" allow="fullscreen"></iframe>', unsafe_allow_html=True)
    
    if st.button("Go Back"):
        st.session_state.page = 'main'

# Main App Logic
if 'page' not in st.session_state:
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    set_css()
    main_content()
elif st.session_state.page == 'Tau_Ceti_E':
    show_360_view('Tau Ceti E', 'https://skybox.blockadelabs.com/e/7ccd18d63ee7d666a128776f4f36f605')
elif st.session_state.page == 'Tau_Ceti_F':
    show_360_view('Tau Ceti F', 'https://skybox.blockadelabs.com/e/06bf286efee8228a4b2fab5299365fc6')
elif st.session_state.page == 'Exoplanet_G':
    show_360_view('Exoplanet G', 'https://skybox.blockadelabs.com/e/5138b576bbffd892de4dda11d5ef25a8')
