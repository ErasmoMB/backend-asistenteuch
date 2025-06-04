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

@router.get('/all')
def get_all_data():
    data = load_data()
    if data is None:
        raise HTTPException(status_code=500, detail="Data not found or could not be loaded")
    return JSONResponse(content=data)

@router.get('/carreras')
def get_carreras():
    data = load_data()
    if data is None or 'carreras' not in data:
        raise HTTPException(status_code=404, detail="Career data not found or could not be loaded")
    return JSONResponse(content=data['carreras'])

@router.get('/admision')
def get_admision():
    data = load_data()
    if data is None or 'admision' not in data:
        raise HTTPException(status_code=404, detail="Admission data not found or could not be loaded")
    return JSONResponse(content=data['admision'])

@router.get('/facultades')
def get_facultades():
    data = load_data()
    if data is None or 'facultades' not in data:
        raise HTTPException(status_code=404, detail="Faculty data not found or could not be loaded")
    return JSONResponse(content=data['facultades'])

@router.get('/servicios')
def get_servicios():
    data = load_data()
    if data is None or 'servicios' not in data:
        raise HTTPException(status_code=404, detail="Service data not found or could not be loaded")
    return JSONResponse(content=data['servicios'])

@router.get('/info')
def get_info():
    """Devuelve información institucional extendida (misión, visión, autoridades, etc)."""
    data = load_data()
    if data is None:
        raise HTTPException(status_code=500, detail="Data not found or could not be loaded")
    # Información adicional hardcodeada (puedes moverla a uch_data.json si prefieres)
    info_extra = {
        "quienes_somos": "La Universidad de Ciencias y Humanidades es una Asociación Civil sin fines de lucro. Es una comunidad académica orientada a la investigación a través de una formación profesional humanista, científica y tecnológica, con una clara conciencia de nuestro país como realidad multicultural. En ese sentido busca favorecer la formación integral de sus estudiantes con un elevado nivel académico e investigativo, con un profundo sentido crítico que ahonda en el conocimiento de nuestra realidad nacional y mundial, promoviendo en ellos el desarrollo de una conciencia solidaria para que actúen con compromiso y responsabilidad social. Fue creada por resolución 0411 del Consejo Nacional para la Autorización de Funcionamiento de Universidades (CONAFU) el 03 de julio del 2006; asimismo, a través de la resolución N° 071-2017, publicada el 21 de noviembre de 2017 en el diario oficial El Peruano, la Superintendencia Nacional de Educación Superior Universitaria (Sunedu) otorgó el licenciamiento institucional, tras culminar con éxito este procedimiento de carácter obligatorio para todas las casas de estudios superiores del país. La UCH surge para brindar una formación integral que abarque no sólo el ámbito académico, sino también el cultivo de las artes y la cultura, el conocimiento de nuestra realidad social y el compromiso con la comunidad.",
        "mision": "Somos una Universidad que forma profesionales mediante una propuesta de educación integral, desarrolla investigación, promueve la cultura y la proyección social; con el fin de contribuir al desarrollo social y productivo del país.",
        "vision": "Ser una Universidad referente en la investigación y la formación integral de profesionales comprometidos con el desarrollo del país.",
        "objetivos": [
            "Formar profesionales de alta calidad científica, humanística y tecnológica que contribuyan con el desarrollo y bienestar del país.",
            "Promover y realizar investigación científica, humanística y tecnológica, teniendo en cuenta la problemática local, regional y nacional.",
            "Extender su área de acción, sus servicios a la comunidad y promover su desarrollo integral.",
            "Desarrollar una firme conciencia en la defensa, fortalecimiento y difusión del patrimonio cultural del país, de sus recursos naturales y de sus productos."
        ],
        "principios": [
            "Búsqueda de la verdad, producción y difusión de nuevos conocimientos fomentando el estudio de la realidad.",
            "Libertad de pensamiento, de crítica, de expresión y de cátedra como manifestaciones del pluralismo intelectual.",
            "Participación democrática a todo nivel, orientada al cumplimiento de los fines institucionales en su proyección a la sociedad.",
            "Preocupación por la problemática universitaria y atención permanente a la realidad económica, política y social del país.",
            "Proyección social universitaria, entendida como la transmisión recíproca de los conocimientos, valores y producción cultural entre la Comunidad y la Universidad.",
            "Vinculación estrecha de la teoría y la práctica como base de la formación profesional y del proceso del conocimiento científico."
        ],
        "autoridades": [
            {"nombre": "Dr. Alfredo Jose Pipa Carhuapoma", "cargo": "Rector", "resolucion": "Resolución N° 109-2023 UC-UCH"},
            {"nombre": "Dr. Fernando Alvarado Rojas", "cargo": "Vicerrector", "resolucion": "Resolución N° 112-2023-CU-UCH"},
            {"nombre": "Dr. Laberiano Matías Andrade Arenas", "cargo": "Decano de la Facultad de Ciencias e Ingeniería"},
            {"nombre": "Dr. Hipólito César Reyes Del Carmen", "cargo": "Decano de la Facultad de Ciencias Contables, Económicas y Financieras"},
            {"nombre": "Dr. Eleazar Armando Flores Medina", "cargo": "Decano de la Facultad de Ciencias de la Salud"},
            {"nombre": "Dr. William Cortez Maldonado", "cargo": "Decano de la Facultad de Humanidades y Ciencias Sociales"}
        ]
    }
    return JSONResponse(content={"info": info_extra, **data})
