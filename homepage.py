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

if 'show_video' not in st.session_state:
    st.session_state.show_video = True

if 'show_button' not in st.session_state:
    st.session_state.show_button = True

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["About", "Play", "Contact"])

# About Tab
with tab1:
    st.markdown("<div id='about_Content'>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # About Contact Section
    st.markdown(
        """
        <div id="about_contact">
            <br>
            <center>
                <p>Team Exo-Explore submitted this website to the 2024 NASA Space App: Exosky Challenge.</p>
                <p>At <b>Stellar Explorers</b>, we invite you to embark on a cosmic adventure like no other.</p>
                <p>Guided by <b>Stella</b>, your mission is to explore distant exoplanets and uncover the mysteries of the stars.</p>
                <p>As an astronaut chosen for this extraordinary task, you’ll navigate through a holographic star map, selecting from ten neighboring stars, each with the potential to host new worlds.</p>
                <p>Your exploration is vital to humanity's future, as you help identify planets that could one day sustain life.</p>
                <p>Begin your journey, and let's chart the unknown together!</p>
            </center>
            <br>
        </div>
        """, unsafe_allow_html=True
    )

# Play Tab
with tab2:
    # Intro section
    st.markdown("<div id='intro_Content'>", unsafe_allow_html=True)
      
    # Sample video data (local file or URL)
    data = "Welcome3.mp4"
    image_data = "shrek.jpg"
    
    # Check session state to show/hide video or image
    if st.session_state.show_video:
        # CSS for video container
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
    if st.session_state.show_button and st.button("Play"):
                st.session_state.show_video = False  # Hide video
                st.session_state.show_button = False  # Hide button
                st.image(image_data, caption="This is the image displayed after the video.")  # Show image
    else:
                # Display the image if the video is hidden
                st.image(image_data, caption="This is the image displayed after the video.")


# Contact Tab
with tab3:
    st.markdown(
        """
        <div id="contact_Content">
            <br>
            <center>
                <p>Contact information is currently redacted.</p>
            </center>
            <br>
        </div>
        """, unsafe_allow_html=True
    )