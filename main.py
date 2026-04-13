from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def data_load():
    with open("patients.json", "r") as f:
        return json.load(f)

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
    patient_id: str = Path(..., description="Patient id in DB", example="P002")
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
