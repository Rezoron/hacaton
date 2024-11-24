from fastapi import FastAPI, File, UploadFile, staticfiles
from .utils import init_file
import asyncio
from pydantic import BaseModel
from typing import List
import os


import os

# Получаем список содержимого текущей директории
contents = os.listdir('uploads')
print(contents)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = FastAPI()
app.mount("/uploads", staticfiles.StaticFiles(directory="uploads"), name="uploads")


class Image(BaseModel):
    url: str
    id: str


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_name_data = file.filename.split('.')

    file_name = '.'.join(file_name_data[:-1])

    base_path = os.path.join("uploads", file_name)

    if not os.path.isdir(base_path):
        os.makedirs(base_path)

    with open(os.path.join(base_path, file.filename), "wb") as f:
        f.write(await file.read())

    asyncio.create_task(init_file(file_name_data, file.size))

    return {"filename": file.filename}


@app.get("/listitem")
async def get_list_img():
    list = []
    for i in os.listdir('uploads'):
        list.append({'url': f'uploads/{i}/1/{i}.jpeg', 'id': i})
    return list
