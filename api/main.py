from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="contraloria"
)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O reemplaza "*" con los orígenes permitidos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # O restringe los métodos permitidos
    allow_headers=["*"],  # O reemplaza "*" con los encabezados permitidos
)

@app.get("/distritos/")
async def get_items():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM info_distrito")
    items = cursor.fetchall()
    return items