from fastapi import APIRouter,Form, HTTPException ,Query
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import os

routes=APIRouter()

@routes.post("/escribir/")
async def prueba(request: str):
    # Utilizamos los atributos del objeto `request` para llamar a la función
    a=""
    return {"message": "Se escribió en el PDF"}