import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Flask Website", layout="wide")

# Injecting combined CSS styles
st.markdown(
    """
    <style>
        /* Link Behaviors */
        a:link, a:visited, a:hover, a:active {
            text-decoration: none;
            color: white;
        }

        /* Background and Text background-color: black;*/
        .main {
            background-image: url('starsImage.jpg'); /* Ensure this path is correct */
            color: white;
            
        }

        /* Custom Main Section Layout */
        .navigation_Bar {
            padding: 1%;
            border-top: 1px solid white;
            width: 30%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 100%;  
        }

        .stTabs[role="tablist"] {
            justify-content: center;        
        }

        .stTitle {
            justify-content: center;
        }

        /* Body: Content Sections */
        #intro_Content, #contact_Content, #about_Content {
            width: 50%;
            height: 100%;
            text-align: center;
            margin: auto;
        }

        /* Play Button */
        #play_Button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            display: inline-block;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px;
        }


        .stTabs [role="tablist"] {
            display: flex;
            justify-content: center;
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
    #st.header("About")
    st.write("This section will provide information about Exo-Explore.")
    st.markdown("</div>", unsafe_allow_html=True)

# Play Tab
with tab2:
    # Intro section
    st.markdown("<div id='intro_Content'>", unsafe_allow_html=True)
    st.write("This section will allow you to play the video.")
    
    
    # Define a function to be triggered when the button is clicked
    def on_button_click():
        st.write("You clicked the Play button!")
        
    # Sample video data (local file or URL)
    data = "Welcome3.mp4"
    
    # CSS to control video size (70% width, 40% height)
    st.markdown(
        """
        <style>
        .video-container {
            max-width: 70%;
            height: auto;
            margin: auto;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Display the video inside the custom-sized container
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    st.video(data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Button and action
    if st.button("Play"):
        on_button_click()
