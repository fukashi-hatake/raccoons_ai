from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel 

import pandas as pd 
from sentence_transformers import SentenceTransformer, util
  

def return_road_jarimalar(user_query): 
    top_k = 1 
    jarimalar_emb_data = pd.read_csv("data/embedded_jarimalar.csv")  

    model = SentenceTransformer('all-MiniLM-L6-v2')  

    jarimalar_emb_data['embedding'] = jarimalar_emb_data['Qoidabuzarlik'].apply(lambda x: model.encode(x, convert_to_tensor=True)) 

    query_embedding = model.encode(user_query, convert_to_tensor=True) 

    scores = jarimalar_emb_data['embedding'].apply(lambda x: util.pytorch_cos_sim(query_embedding, x).item())
    top_matches = jarimalar_emb_data.iloc[scores.nlargest(top_k).index] 

    return {
        "Qonunbuzarlik": top_matches.Qoidabuzarlik.iloc[0], 
        "Jarima (BHM)": top_matches.jarima_bhm.iloc[0], 
    }



def return_tadbirkorlik_lex(user_query): 
    top_k = 1 
    tadbirkorlik_emb_data = pd.read_csv("data/tadbirkorlik.csv")  

    model = SentenceTransformer('all-MiniLM-L6-v2')  

    tadbirkorlik_emb_data['embedding'] = tadbirkorlik_emb_data['Context'].apply(lambda x: model.encode(x, convert_to_tensor=True)) 

    query_embedding = model.encode(user_query, convert_to_tensor=True) 

    scores = tadbirkorlik_emb_data['embedding'].apply(lambda x: util.pytorch_cos_sim(query_embedding, x).item())
    top_matches = tadbirkorlik_emb_data.iloc[scores.nlargest(top_k).index] 

    return {
        "Sarlavha": top_matches.Title.iloc[0], 
        "Havola": top_matches.Link.iloc[0], 
    }


def return_konstitutsiya(user_query): 
    top_k = 1 
    konstitutsiya_data = pd.read_csv("data/konstitutsiya.csv")  

    model = SentenceTransformer('all-MiniLM-L6-v2')  

    konstitutsiya_data['embedding'] = konstitutsiya_data['modda'].apply(lambda x: model.encode(x, convert_to_tensor=True)) 

    query_embedding = model.encode(user_query, convert_to_tensor=True) 

    scores = konstitutsiya_data['embedding'].apply(lambda x: util.pytorch_cos_sim(query_embedding, x).item())
    top_matches = konstitutsiya_data.iloc[scores.nlargest(top_k).index] 

    return {
        "Modda": top_matches.raqam.iloc[0], 
        "To'liq": top_matches.modda.iloc[0], 
    } 



app = FastAPI()

class Road_Fine(BaseModel):
    query: str


class Tadbirkorlik(BaseModel):
    query: str


class Konstitutsiya(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"Qonunchilik": "ChatBot"}


@app.post("/road_fine/") 
def get_road_fine_query(item: Road_Fine): 
    return return_road_jarimalar(item.query)


@app.post("/tadbirkorlik/") 
def get_tadbirkorlik_query(item: Tadbirkorlik): 
    return return_tadbirkorlik_lex(item.query)


@app.post("/konstitutsiya/") 
def get_konstitutsiya_query(item: Konstitutsiya): 
    return return_konstitutsiya(item.query)
