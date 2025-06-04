from fastapi import APIRouter, HTTPException
import json
import os
from fastapi.responses import JSONResponse

router = APIRouter()

DATA_FILE = os.path.join(os.path.dirname(__file__), 'uch_data.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data file {DATA_FILE}: {e}")
        return None

@router.get('/api/all')
def get_all_data():
    data = load_data()
    if data is None:
        raise HTTPException(status_code=500, detail="Data not found or could not be loaded")
    return JSONResponse(content=data)

@router.get('/api/carreras')
def get_carreras():
    data = load_data()
    if data is None or 'carreras' not in data:
        raise HTTPException(status_code=404, detail="Career data not found or could not be loaded")
    return JSONResponse(content=data['carreras'])

@router.get('/api/admision')
def get_admision():
    data = load_data()
    if data is None or 'admision' not in data:
        raise HTTPException(status_code=404, detail="Admission data not found or could not be loaded")
    return JSONResponse(content=data['admision'])

@router.get('/api/facultades')
def get_facultades():
    data = load_data()
    if data is None or 'facultades' not in data:
        raise HTTPException(status_code=404, detail="Faculty data not found or could not be loaded")
    return JSONResponse(content=data['facultades'])

@router.get('/api/servicios')
def get_servicios():
    data = load_data()
    if data is None or 'servicios' not in data:
        raise HTTPException(status_code=404, detail="Service data not found or could not be loaded")
    return JSONResponse(content=data['servicios'])
