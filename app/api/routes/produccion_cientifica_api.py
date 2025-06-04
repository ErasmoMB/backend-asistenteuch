from fastapi import APIRouter, HTTPException
import json
import os
from fastapi.responses import JSONResponse

router = APIRouter()

DATA_FILE = os.path.join(os.path.dirname(__file__), 'produccion_cientifica_uch.json')

def load_produccion_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data file {DATA_FILE}: {e}")
        return None

@router.get('/produccion_cientifica')
def get_produccion_cientifica():
    data = load_produccion_data()
    if data is None:
        raise HTTPException(status_code=500, detail="Data not found or could not be loaded")
    return JSONResponse(content=data)
