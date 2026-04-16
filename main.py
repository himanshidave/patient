from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field ,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):

    id:Annotated[str, Field(..., description="ID of patients")]
    name:str
    age:int
    city:str
    gender:Annotated[Literal["male","female","Other"],Field(...,description="Gender of patient")]
    height:float
    weight:float

    @computed_field
    @property
    def bmi(self)-> float:
        bmi=(self.weight/(self.height**2))
        return bmi
    

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "underweight"
        
        elif self.bmi <25:
            return "normal"
        
        elif self.bmi <30:
            return "normal"
        
        else:
            return "Obese"


def data_load():
    with open("patients.json", "r") as f:
        return json.load(f)
    

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f)

@app.get("/")
def home():
    return {"msg": "Patient management system"}

@app.get('/about')
def about():
    return {"msg": "API to manage patients records"}

@app.get("/view")
def view():
    return data_load()

@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="Patient id in DB", examples="P002")
):
    data = data_load()

    for patient in data:
        if patient["id"] == patient_id:
            return patient
    
    raise HTTPException(status_code=404 ,detail="Patient not found")

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by field (height, weight, bmi)"),
    order: str = Query("asc", description="Sort order: asc or desc")
):
    data = data_load()

    valid_fields = ["height", "weight", "bmi"]

    # validate field
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose from {valid_fields}"
        )

    # validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Use 'asc' or 'desc'"
        )

    # sorting logic
    reverse = True if order == "desc" else False

    sorted_data = sorted(
        data,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )

    return sorted_data

@app.post("/create")
def create_pateint(patient:Patient):


    #Load data
    data=data_load

    #check if patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")
    

    #add new patient to DB
    data[patient.id]=patient.model_dump(exclude=["id"])#convert pydantic object into dict

    #save to json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message":"patient created successfully"})
