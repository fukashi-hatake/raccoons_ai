import streamlit as st 
import requests

URL = "http://127.0.0.1:8000/" 
ROAD_FINE_END = "road_fine/"
BHM = 375000  

def constitution_chat(): 
    st.sidebar.link_button("📌 Rasmiy uzpdd.uz saytiga o'tish", "https://uzpdd.uz/") 
    st.sidebar.info("BHM (Bazaviy hisoblash miqdori) = 375,000 so'm")
    
    st.chat_message("assistant").write("Sizga yo'l harakatidagi jarimalar haqida qanday yordam bera olaman?") 
    st.markdown("***") 

    # if "messages" not in st.session_state:
    #    st.session_state.messages = []
 
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

        response = requests.post(f"{URL}{ROAD_FINE_END}", json=data)
        if response.status_code == 200: 
            javob = response.json()

            assistant_response = f"{response.json()['Qonunbuzarlik']}, Jarimasi {response.json()['Jarima (BHM)']} BHM = {response.json()['Jarima (BHM)']*BHM} so'm"
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.chat_message("assistant").write(assistant_response)


if __name__ == '__main__':
    # st.session_state.messages = []
    constitution_chat()