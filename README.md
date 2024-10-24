# Check out Our website! 
We are proud to showcase our website! 
https://2024-nasa-challenge-spaceapp-zcgdlqnf4kuvg5urwvp45q.streamlit.app/ 

# SpaceApp2024
NASA Seattle Space App Challenge 2024

Our project is a web-based game designed using Streamlit that invites middle school students to embark on a virtual astronaut mission to explore exoplanets and chart stars for future space explorers. By incorporating data from NASA and Gaia Data Release 3 (Gaia DR3), students can interact with a 3D model of a chosen exoplanet and view its terrain from an astronaut’s perspective. The game introduces players to Stella, an AI guide, who helps them navigate the experience, starting with selecting a star and exoplanet from our galaxy. Players can explore the exoplanet’s surface through AI-generated renderings or view an interactive star map based on Gaia DR3 data, where they can create personalized constellations. This project aims to ignite interest in space exploration and STEM education while making the game accessible to students worldwide via a web-app format. Future versions will expand AI features, including real-time chatbots, sign language translations, and enhanced accessibility tools. Developed primarily in Python, the project utilizes NASA’s Eyes on Exoplanets, Streamlit, Anaconda, Github, and Visual Studio Code for development and testing.

# Connecting Github to VSC
1) **Download and Install Anaconda:** Visit the [Anaconda website](https://www.anaconda.com/download) and download the installer for your specific operating system.
2) **Install Anaconda:** During installation, keep everything set to the default settings.
3) **Install Jupyter and Visual Studio Code via Anaconda Navigator:**
    * Jupyter is useful for running small amounts of code.
    * Visual Studio Code is ideal for larger projects.
4) **Create a Folder:** Set up a folder to store the project code.
5) **Source Control in Visual Studio Code:**
    * Open Visual Studio Code and navigate to the **Source Control** tab.
    * Select **Clone Repository** and enter the GitHub URL for the repository.
6) **Select a Folder for GitHub Code:** Choose the folder where you want to store the cloned GitHub repository.
7) **Open the Folder in Visual Studio Code:** In Visual Studio Code, go to **File → Open Folder**, and select the folder where the GitHub code was saved.


# To Edit the Github Code in visual Studio Code 
1) **Open Anaconda and Launch VScode**
2) Open a termainal in viual studio code and install streamlit, astroquery, and streamlit-drawable-canvas 
    * to install astroquery type `pip install astroquery`
       * astroquery is used to create access NASA database 
    * to install streamlit type `pip install streamlit`
        * streamlit is used to create a website using python 
    * to install streamlit-drawable-canvas type `pip install streamlit-drawable-canvas`
        * streamlit-drawable-canvas is used for drawing on the starchart 
    * to install pipreqs type `pip install pipreqs` 
        * pipreqs is used to publish the streamlit website  
3) **Run the Code:** Open the terminal in Visual Studio Code go to proper directory and type the following to execute the code.
4) `streamlit run .\homepage.py` 

# To Edit the Github Code in Jupyter 
1)  Open **Anaconda** > Launch **Jupyter Notebook** > Navigate to your directory for the space apps project.
2) Open the Python file (with the `.py` extension) or both the `.py` and `.ipynb` files if needed.
3) Open the terminal in Jupyter Notebook while in the project directory.
4) Use the terminal to run `pip install` for any required packages not included with Anaconda.
5) Once all the packages are installed, run the code or app to ensure everything works correctly.

**Note**: The `.ipynb` format is highly recommended for step-by-step code execution and debugging. It provides better visibility into your workflow.



