from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class Calificacion(BaseModel):
    pregunta1: int
    pregunta2: int
    pregunta3: int

@app.post("/guardar-calificacion")
def guardar_calificacion(datos: Calificacion):
    print("Recibido:", datos)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1-3-2005",
        database="stopfraude"
    )
    cursor = conn.cursor()
    query = "INSERT INTO calificacion (id_pregunta, estrellas) VALUES (%s, %s)"
    valores = [
        (1, datos.pregunta1),
        (2, datos.pregunta2),
        (3, datos.pregunta3)
    ]
    cursor.executemany(query, valores)
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "ok"}
