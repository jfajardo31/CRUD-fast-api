import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from routes.routes import routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "Title API"
app.version = "0.0.1"
app.description = "API description"

app.include_router(routes)


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
    return HTMLResponse("<h1>Title API</h1>")
    #return f"Container ID: {socket.gethostname()}"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)