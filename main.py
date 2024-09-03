import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from routers.cognitive_router import cognitive_router

app = FastAPI()
app.title = "Title API"
app.version = "0.0.1"
app.description = "API description"

app.include_router(cognitive_router)

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