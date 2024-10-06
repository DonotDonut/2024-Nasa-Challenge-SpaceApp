import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Flask Website", layout="wide")

# Injecting custom CSS styles
st.markdown(
    """
    <style>
    /* Link Behaviors */
    a:link {text-decoration: none; color: white;}
    a:visited {text-decoration: none; color: white;}
    a:hover {text-decoration: none; color: white;}
    a:active {text-decoration: none; color: white;}

    /* Header */
    .navigation_Bar {
        padding: 1%;
        border-top: 1px solid white;
        margin: 0;
        width: 30%;
        height: auto;
        top: 25%;
        display: flex;
        font-size: 100%;
        justify-content: centered;
        align-items: center; 
    }

    /* Body: Main */
    body {
        background-image: url('starsImage.jpg'); /* Use a valid image URL or path */
        color: white;
        overflow: hidden;
    }

    .main {
        width: 100%;
        height: 70%;
        display: flex;
        justify-content: center;
        align-items: center; /* Center vertically */
    }

    #intro_Content, #contact_Content, #about_Content {
        width: 50%;
        height: 100%;
        text-align: center;
    }

    #intro_Video {
        padding: 10px 20px;
        border-radius: 5px;
        position: relative;
        width: 80%;
        height: auto; /* Maintain aspect ratio */
    }

    #play_Button {
        align-items: center;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        size: 50%;
    }

    /* Footer */
    .footer {
        justify-content: center;
        width: 100%;
        height: auto;
        text-align: center;
        margin-top: 20px; /* Space above footer */
        background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("EXO-EXPLORE")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["About", "Play", "Contact"])

# About Tab
with tab1:
    st.markdown("<div id='about_Content'>", unsafe_allow_html=True)
    st.write("### About")
    st.write("This section will provide information about Exo-Explore.")
    st.markdown("</div>", unsafe_allow_html=True)

# Play Tab
with tab2:
    st.markdown("<div id='intro_Content'>", unsafe_allow_html=True)
    st.write("### Play")
    st.write("This section will allow you to play the video.")
    
    # Video Section
    st.video("https://yourdomain.com/path/to/sample-video.mp4")  # Replace with the actual URL or local path

    # Play Button (Using Streamlit's button functionality)
    if st.button("Play", key='play_button'):
        st.success("Button clicked!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Contact Tab
with tab3:
    st.markdown("<div id='contact_Content'>", unsafe_allow_html=True)
    st.write("### Contact")
    st.write("This section will provide contact information.")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Team Exo-Explore submitted this website to the 2024 NASA Space App: Exosky Challenge</div>', unsafe_allow_html=True)
