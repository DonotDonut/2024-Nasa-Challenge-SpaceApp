import streamlit as st
import openai
import os

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Session state to store chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to generate a response from OpenAI
def generate_response(user_input):
    # Construct the prompt
    messages = [
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    return response['choices'][0]['message']['content']

def main():
    st.title("Simple Chatbot")

    # Chat container
    st.markdown('<div style="position: fixed; bottom: 20px; right: 20px; width: 300px; background-color: #ffffff; border: 1px solid #ccc; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); padding: 10px; z-index: 1000;">', unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.messages:
        role = msg['role']
        content = msg['content']
        st.markdown(f"<strong>{role.capitalize()}:</strong> {content}", unsafe_allow_html=True)

    user_input = st.text_input("You:", "", key="user_input")

    if st.button("Send"):
        if user_input:
            # Save user message to session state
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = generate_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Clear the input field
            st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
