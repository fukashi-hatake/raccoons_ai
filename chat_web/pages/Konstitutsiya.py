import streamlit as st 
import requests

URL = "http://127.0.0.1:8000/" 
CONSTITUTION_END = "konstitutsiya/"


def constitution_chat(): 
    st.sidebar.link_button("📌 Rasmiy saytga o'tish", "https://lex.uz/docs/-6445145")   
    st.sidebar.image("images/konstitutsiya.png")
    st.sidebar.info("Oʻzbekiston Respublikasining Konstitutsiyasi 1992-yil 8-dekabrda qabul qilingan")
    st.sidebar.info("**Konstitutsiya**: (lotincha: constitutio — „o'rnatish“, „belgilash“) — bu davlatning asosiy bosh qonuni.")

    st.chat_message("assistant").write("Sizga konstitutsiyamiz haqida qanday yordam bera olaman?") 
    st.markdown("***") 

    if "messages" not in st.session_state:
       st.session_state.messages = []
 
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

        response = requests.post(f"{URL}{CONSTITUTION_END}", json=data)
        if response.status_code == 200: 
            javob = response.json()

            assistant_response = f"{javob['Modda']}-modda: {javob['Toliq']}"
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.chat_message("assistant").write(assistant_response)


if __name__ == '__main__':
    # st.session_state.messages = []
    constitution_chat()