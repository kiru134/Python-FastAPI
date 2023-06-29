
from routers import blog_get, blog_post, users, article, products, file, dependencies
from auth import authentication
from fastapi import FastAPI, Request, HTTPException
from db.database import engine
from db import models
from exceptions import StoryException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from templates import templates
import time
from client import html
from fastapi.websockets import WebSocket


app = FastAPI()
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(file.router)
app.include_router(authentication.router)
app.include_router(products.router)
app.include_router(article.router)
app.include_router(users.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time()-start_time
    response.headers['duration'] = str(duration)
    return response


@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []


@app.websocket("/chat")
async def websoket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exe: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exe.name}
    )


# @app.exception_handler(HTTPException)
# def custom_handker(request: Request, exe: StoryException):
#     return PlainTextResponse(str(exe), status_code=400)


models.Base.metadata.create_all(engine)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

# To make files statstically avaialble on localhost we use mount
# app.mount('/files', StaticFiles(directory="files"), name='files')
app.mount('/templates/static',
          StaticFiles(directory="templates/static"), name='static')
