from fastapi import FastAPI
import json


app=FastAPI()

def data_load():
    with open("patients.json","r") as f:
        data = json.load(f)

    return data

@app.get("/")
def home():
    return{"msg":"Patient management system"}

@app.get('/about')
def about():
    return{"msg":"API to manage patients records"}


@app.get("/view")
def view():
    data = data_load()
    return data 
