import streamlit as st
import subprocess

# Set up the page configuration
st.set_page_config(page_title="Flask Website", layout="wide") #THIS LINE MUST BE THE FIRST NO MATTER WHAT!!!    

# Navigation in Streamlit 
st.page_link("homepage.py", label="Home", icon="🏠")
st.page_link("pages/Exoplanet_3D.py", label="Exoplanet_3D", icon="1️⃣")

# Initialize the session state if it doesn't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'  # Default to home page

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
        .main, .stApp {
            background-color: #1a1a1a; /* Dark background */
            color: white; /* White text */
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
            text-align: left;
            margin: auto;
        }

        /*
        #play_Button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            display: inline-block;
            width: 30%;
            height: 20%;
            justify-content:center;
        }
        */

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 20px;
            background-color: #121212;
            padding: 10px;
            color: white; /* White text in footer */
        }
        /*.footer {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            bottom: 0;
            position: fixed;
        }*/

        .stTabs [role="tablist"] {
            display: flex;
            justify-content: center;
        }
        .stTabs button {
            padding: 10px 20px; /* Increase button padding */
            font-size: 24px; /* Increase button text size */
            margin: 0 5px; /* Adjust margin between tabs */
            background-color: transparent; /* Ensure tab background is transparent */
            border: 1px solid white; /* Add border for better visibility */
            border-radius: 5px; /* Rounded corners */
            color: white; /* Text color */
        }
        .stTabs button:hover {
            background-color: rgba(255, 255, 255, 0.1); /* Hover effect */
        }   

        /* PLAY TAB*/
        .video-container {
            max-width: 70%;
            height: auto;
            margin: auto;
        }
         

        /* TEAM MEMBER TAB*/
        .team {
            display: flex;
            flex-direction: column;
            gap: 20px;
            /*background-color: grey;*/ /*Only used for visualizing divs remember to comment out!!*/
            width: 60%;
            text-align: left;
        }

        .member {
            display: flex;
        }

        .memberName, .memberAbout {
            flex: 1;
        }

        .memberName {
            font-weight: bold;
            padding-right: 20px;
        }
        
        
    </style>
    """,
    unsafe_allow_html=True
)

# Header
#st.title("EXO-EXPLORE")

st.markdown(
    """
    <h1 style='text-align: center; font-size: 70px; color: white;'>EXO-EXPLORER</h1>
    """,
    unsafe_allow_html=True
)

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["About", "Play", "Team Members"])

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
                <p>
                    Team Exo-Explorer submitted this website to the 2024 NASA Space App: Exosky Challenge. 
                    <br> <br>
                    We invite you to embark on a cosmic adventure like no other. <br>
                    Guided by our AI, Stella, your mission is to <b>explore distant exoplanets</b> <br>
                    and <b>uncover the mysteries of the stars</b>. As an astronaut chosen for this <br>
                    extraordinary task, you’ll navigate through a holographic star map, selecting  <br>
                    from ten neighboring stars, each with the potential to host new worlds.
                    <br> <br>
                    Your exploration is vital to humanity's future, as you help identify planets that could one day sustain life.
                    <br> <br>
                    Begin your journey, and let's chart the unknown together!
                </p>
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
    
        # CSS for video container
    st.markdown(
            """
                <footer>
                    <br>
                    <center>
                        <p> 
                            Team Exo-Explorer submitted this website to the 2024 NASA Space App: Exosky Challenge.
                        </p>
                    </center>
                </footer>
            """, unsafe_allow_html=True
    )

    # Display the video inside the custom-sized container
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    st.video(data)
    st.markdown('</div>', unsafe_allow_html=True)
    # Function to run another Streamlit app
    def run_other_app():
        # Define the path to your other Streamlit app
        exoplanet_app_path = "pages\Exoplanet_3D.py"

        # Run the other app as a subprocess
        subprocess.Popen(["streamlit", "run", exoplanet_app_path])
    
        # Buttons for navigation in the main content area
    if st.button("Play Now!", ):
        run_other_app()
        st.success("Exoplanet 3D App is now running!")
        
      
        
            

# Contact Tab
with tab3:
    st.markdown(
        """
        <style>
            .team, .team h3, .team p {
                color: white;
            }
        </style>
        <center>
            <div class = "team">
                <div class = "member">
                    <div class = "memberName">
                        <h3> Mathea Caole</h3>
                    </div>
                    <div class = "memberAbout">
                        <p> 
                            Senior undergraduate bioengineer student at the University of Washington. Worked on software, design, and storytelling.
                        </p>
                    </div>
                </div>
                <div class = "member">
                    <div class = "memberName">
                        <h3> Timothy Caole</h3>
                    </div>
                    <div class = "memberAbout">
                        <p> 
                            Graduate student in Electrical and Computer Engineering at the University of Washington and Co-Founder of SommerAI.
                            Worked on web development and documentation strategy with skills in GitHub and file management.
                        </p>
                    </div>
                </div>
                <div class = "member">
                    <div class = "memberName">
                        <h3>Yasin Chowdhury</h3>
                    </div>
                    <div class = "memberAbout">
                        <p> 
                            Applied Physics and Astronomy Graduate from the University of Washington.
                            Experienced in research projects involving asteroid discovery, experimental 
                            nuclear physics, supernovae and gravitational wave detection with LIGO. 
                            Worked on app design, coding, science and various technical projects.
                        </p>
                    </div>
                </div>
                <div class = "member">
                    <div class = "memberName">
                        <h3> Colin Christianson</h3>
                    </div>
                    <div class = "memberAbout">
                        <p> 
                            Founder & CEO of Tenacious Ventures, one of the only live production companies to produce a live 
                            interactive webcast from the moon during the NASA Artemis 1 Callisto Mission. Worked on project 
                            coordination, presentation, GPT creating and training, and AI generated video.
                        </p>
                    </div>
                </div>
                <div class = "member">
                    <div class = "memberName">
                        <h3> Giulianna Gasparotto</h3>
                    </div>
                    <div class = "memberAbout">
                        <p> 
                            Actress, Filmmaker, Writer, Photographer, AI Prompter, AI Designer.
                        </p>
                    </div>
                </div>
                <div class = "member">
                    <div class = "memberName">
                        <h3> Sara Saleh</h3>
                    </div>
                    <div class = "memberAbout">
                        <p> 
                            University of Washington graduate with a Bachelors in Computer Engineering. 
                            Worked on storytelling, design, and coding assistance.
                        </p>
                    </div>
                </div>
            </center>

    
        <footer>
            <br>
            <center>
                <p> 
                    Team Exo-Explorer submitted this website to the 2024 NASA Space App: Exosky Challenge.
                </p>
            </center>
        </footer>
        """, unsafe_allow_html=True
    )
