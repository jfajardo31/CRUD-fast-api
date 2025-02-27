from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from routes.routes import routes,routes_b
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "Práctica CRUD"
app.version = "0.0.1"
app.description = "API description"

#cargar archivo de variables de entorno
load_dotenv()

app.include_router(routes)
app.include_router(routes_b)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE","PATCH"],
    allow_headers=["*"],
)


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Default API",
    tags=["APP"]
)
def message():
    """Home default API

    Returns:
        Message
    """
    return HTMLResponse("<h1>Ejericio de Prueba</h1>")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)