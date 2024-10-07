import streamlit as st
import subprocess



# URL 
#Exoplanet_3D_path = "C:\Users\Tim\Documents\2024 Nasa SpaceApp Challenge\Nasa-Challenge-SpaceApp2024\Exoplanet_3D.py" 

# Set up the page configuration
st.set_page_config(page_title="Flask Website", layout="wide")

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
        .main {
            
            color: black;
            
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
            padding: 10px;
            bottom: 0;
            position: fixed;
        }

        .stTabs [role="tablist"] {
            display: flex;
            justify-content: center;
        }    
    
        /* Team Member Tab*/
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
st.title("EXO-EXPLORE")



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
                    Guided by our AI Stella, your mission is to <b>explore distant exoplanets</b> <br>
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
    # Function to run another Streamlit app
    def run_other_app():
        # Define the path to your other Streamlit app
        exoplanet_app_path = r"C:\Users\Tim\Documents\2024 Nasa SpaceApp Challenge\Nasa-Challenge-SpaceApp2024\website\Exo-Explorer\Exoplanet_3D.py"

        # Run the other app as a subprocess
        subprocess.Popen(["streamlit", "run", exoplanet_app_path])
    
        # Buttons for navigation in the main content area
    if st.button("Play Now!"):
        #st.session_state.current_page = 'exoplanet_3D'  # Set current page to exoplanet_3D
    
        run_other_app()
        st.success("Exoplanet 3D App is now running!")
        
      
        
            

# Contact Tab
with tab3:
    st.markdown(
        """
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
                            Worked on web development and documentation strategy, with skills in GitHub and file management
                        </p>
                    </div>
                </div>
                <div class = "member">
                    <div class = "memberName">
                        <h3>Yasin Chowdhur</h3>
                    </div>
                    <div class = "memberAbout">
                        <p> 
                            University of Washington graduate Astrophysics student. Worked on Design, Coding and technical projects. 
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
                            University of Washington graduate computer engineering student. Worked on storytelling, design, and coding assistance.
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