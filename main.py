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

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
    data = data_load()

    for patient in data:
        if patient["id"] == patient_id:
            return patient
    
    return("Id doesnt exist")