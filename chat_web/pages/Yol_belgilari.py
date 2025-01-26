import streamlit as st  

import streamlit as st
import numpy as np
import torch
from torchvision import datasets, models, transforms
from PIL import Image
import torch.nn.functional as F
import matplotlib.pyplot as plt 

from utils import util  


classes_dict = {0: "50 tezlik", 
                1: "Boshqa xavf-xatar",
                2: "Yo'l bering", 
                3: "Kirish mumkin emas", 
                4: "Piyodalarga yo'l bering", 
                5: "Stop",} 


discription = {"50 tezlik": "Yuqori tezlik cheklangan: Haydovchi harakatning serqatnovligini, transport vositasi va yukning hususiyati hamda holatini, yo'l va ob-havo sharoitini, shuningdek, harakatlanish yo'nalishidagi ko'rinishni hisobga olgan holda transport vositasini belgilangan cheklangan tezlikdan oshirmasdan boshqarishi kerak. Batafsil: https://pdd-uzbeki.narod.ru/speed.htm", 
               "Boshqa xavf-xatar": "Boshqa xavf-xatar: Ogohlanturuvchi belgilarda ko'zda tutilmagan xavf xatarlar bo'lgan yo'l qismi. Batafsil: https://pdd-uzbeki.narod.ru/warn.htm",
               "Yo'l bering": "Yo'l bering: Haydovchi kesib o'tilayotgan yo'ldan, 7.13 qo'shimcha belgisi bo'lganda esa asosiy yo'ldan kelayotgan transport vositasiga yo'l berishi kerak. Batafsil: https://pdd-uzbeki.narod.ru/prefer.htm", 
               "Kirish mumkin emas": "Kirish ta'qiqlangan: Barcha transport vositalarining kirishi taqiqlangan. Batafsil: https://pdd-uzbeki.narod.ru/tabu.htm", 
               "Piyodalarga yo'l bering": "Piyodalarning o'tish joyi: Transport vositasining haydovchisi tartibga solinmagan piyodalar o'tish joyida qatnov qismidan o'tayotgan piyodalarga yo'l berishi shart. https://uzavtoyolbelgi.uz/uz/dorojnie/znaki", 
               "Stop": "To’xtamasdan harakatlanish taqiqlangan: To'xtash chizig'i oldida, agar u bo'lmasa, kesib o'tiladigan qatnov qismining chetida to'xtamasdan harakatlanish taqiqlanadi. Haydovchi kesib o'tilayotgan yo'lda 7.13 qo'shimcha belgisi bo'lganda esa asosiy yo'ldan chiqayotgan transport vositalariga yo'l berish kerak. Batafsil: https://pdd-uzbeki.narod.ru/prefer.htm"} 


normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
input_size = 280 


def load_model(): 
    model_ft = torch.load("models/traffic_sign_model.pth", map_location=torch.device('cpu')) 
    return model_ft



def process_image(input_image): 
    data_transforms = transforms.Compose([ 
        util.Resize(size=input_size), 
        transforms.ToTensor(),
        util.Pad(input_size),
        normalize])  
    

    input_tensor = data_transforms(input_image)
    input_batch = input_tensor.unsqueeze(0).numpy().astype(np.float32)  

    input = input_batch[0].transpose((1, 2, 0))

    return input_tensor 


def predict(model, input_tensor, classes): 
    prediction_dict = {} 
    sigmoid_preds = {}
    temperatured_dict = {}

    pred_pure = model(input_tensor.unsqueeze(0))
    pred = F.softmax(pred_pure, dim=1)   

    for i in range(len(classes)):
        prediction_dict[classes[i]] = round(float(pred[0][i]) * 100, 2) 
        sigmoid_preds[classes[i]] = round(float(pred_pure[0][i]), 2)

    prediction_dict = dict(sorted(prediction_dict.items(), key=lambda item: item[1], reverse=True))
    sigmoid_prediction_dict = dict(sorted(sigmoid_preds.items(), key=lambda item: item[1], reverse=True)) 

    temperature = 1.5  # Adjust temperature for softening
    scaled_logits = pred_pure / temperature
    probabilities = F.softmax(scaled_logits, dim=1)

    for i in range(len(classes)):
        temperatured_dict[classes[i]] = round(float(probabilities[0][i]) * 100, 2) 
    
    temperatured_dict = dict(sorted(temperatured_dict.items(), key=lambda item: item[1], reverse=True))

    return prediction_dict 




def road_signs(): 
    st.sidebar.link_button("📌 Rasmiy uzavtoyolbelgi.uz saytiga o'tish", "https://uzavtoyolbelgi.uz/uz/dorojnie/znaki") 
    st.sidebar.image("images/1200x630wa.png") 
    
    st.chat_message("assistant").write("Sizga yo'l belgisi topishda yordam beraman!") 
    st.markdown("***") 

    uploaded_image = st.file_uploader("Rasm kiriting") #  type=["png", "jpg", "jpeg"]  

    if uploaded_image: 
        model = load_model() 
        input_image = Image.open(uploaded_image)  
        col1, col2 = st.columns(2)
        col1.image(uploaded_image, caption="Input image", use_column_width=True)

        input_image = process_image(input_image) 

        prediction = predict(model, input_image, classes_dict) 

        pred = next(iter(prediction)) 

        st.chat_message("assistant").write(f"Menimcha bu **{pred}** belgisi!") 
        st.chat_message("assistant").write(f"{discription[pred]}")  




if __name__ == '__main__':
    st.session_state.messages = []
    road_signs()