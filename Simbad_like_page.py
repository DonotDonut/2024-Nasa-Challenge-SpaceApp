import streamlit as st

# Set up the Streamlit app
st.title("Interactive Sky Viewer - Aladin Lite")

# Embed the Aladin Lite sky viewer using an iframe
aladin_iframe = """
<iframe frameborder="0" style="width: 100%; height: 500px" src="https://aladin.u-strasbg.fr/AladinLite/?target=CP+Lac&fov=0.5&survey=P/DSS2/color"></iframe>
"""

# Display the Aladin Lite iframe in Streamlit
st.components.v1.html(aladin_iframe, height=500)
