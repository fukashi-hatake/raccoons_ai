import streamlit as st 
import requests

URL = "http://127.0.0.1:8000/" 
BUSINESS_END = "tadbirkorlik/"


def business_related_rules(): 
    st.sidebar.link_button("📌 Rasmiy lex.uz saytiga o'tish", "https://lex.uz/")  

    st.chat_message("assistant").write("Sizga tadbirkorlik bo'yicha qanday yordam bera olaman?") 
    st.markdown("***")
 
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        elif message["role"] == "user":
            st.chat_message("user").write(message["content"])

    prompt = st.chat_input("Savolingizni yozing")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        data = {"query": prompt}

        response = requests.post(f"{URL}{BUSINESS_END}", json=data)
        if response.status_code == 200: 
            javob = response.json()

            assistant_response = f"Sarlavha: {response.json()['Sarlavha']}, Havola: {response.json()['Havola']}"
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.chat_message("assistant").write(assistant_response)


if __name__ == '__main__':
    # st.session_state.messages = []
    business_related_rules()