from fastapi import FastAPI, WebSocket
from app.api import router
from fastapi.staticfiles import StaticFiles
from scripts.setup_database import setup_database
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from app.websocket import websocket_exception_handler, websocket_endpoint


app = FastAPI()
setup_database()
app.include_router(router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# Настройте CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(WebSocketDisconnect)
async def websocket_error_handler(request, exc):
    return await websocket_exception_handler(request, exc)


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    return await websocket_endpoint(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
