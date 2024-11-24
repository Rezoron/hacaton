from fastapi import FastAPI, Request, staticfiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import requests
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/list", response_class=HTMLResponse)
async def about(request: Request):
    if (request := requests.get("127.0.0.1:8000/listitem")).status_code == 200:
        return templates.TemplateResponse("list.html", {"request": request, 'imgs': json.load(request.json())})
    else:
        return templates.TemplateResponse("list.html", {"request": request})