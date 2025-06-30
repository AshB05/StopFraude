from fastapi import FastAPI
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv 

load_dotenv()

api_key = os.getenv("APP_API_KEY")

if not api_key:
    raise ValueError("La variable de entorno APP_API_KEY no está configurada.")

client = OpenAI(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica la URL de tu frontend, por ejemplo: ["http://localhost:8000", "http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

    
@app.get("/Detector_Fraude/{texto}")
async def analizar_texto(texto: str):
    prompt = (
        f"Analiza el siguiente texto: \"{texto}\"\n\n"
        "1. Analizar que nivel de riesgo tiene el mensaje decir si es bajo medio o alto .\n"
        "2. decir que probabilidad de fraude tiene en porcentaje.\n"
        "3. motivos porla cual se considera que se esta considerando fraude.\n"
        "4. recomendaciones par evitar el fraude.\n "
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        resultado = response.choices[0].message.content
        return {"analisis_resultado": resultado}
    except Exception as e:
        print(f"Error al comunicarse con la API de OpenAI: {e}")
        return {"error": "No se pudo completar el análisis, intenta de nuevo más tarde."}, 500

