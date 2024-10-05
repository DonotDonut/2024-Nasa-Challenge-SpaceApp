import streamlit as st
import pandas as pd
import openai
import os


def load_data(file):
    if file is not None:
        data = pd.read_csv(file)
        return data
    return None

def main():
    st.title("Custom GPT Chatbot")

    uploaded_file = st.file_uploader("2024-10-05T19-18_export.csv", type="csv")
    data = load_data(uploaded_file)

    if data is not None:
        st.write("Data Loaded:")
        st.dataframe(data)

    user_input = st.text_input("You:", "")
    
    if st.button("Send"):
        if data is not None:
            response = generate_response(user_input, data)
            st.text_area("GPT:", response, height=200)

def generate_response(user_input, data):
    # Here you can create a custom context based on your data
    context = "You are a knowledgeable assistant. Here are some facts:"
    
    for index, row in data.iterrows():
        context += f"\n{row['input']} - {row['output']}"

    full_prompt = f"{context}\nUser: {user_input}\nAssistant:"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    main()
