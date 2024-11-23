from fastapi import FastAPI, File, UploadFile
import os
from .utils import init_file
import asyncio

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = FastAPI()


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
