from fastapi import FastAPI, File, UploadFile
import uuid
import os
from app.utils import init_file
import asyncio

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_name_data = file.filename.split('.')

    file_name = '.'.join(file_name_data[:-1])

    if not os.path.isdir(os.path.join("uploads", file_name)):
        os.makedirs(f"uploads/{file_name}")
    
    with open(f"uploads/{file_name}/{file.filename}", "wb") as f:
        f.write(await file.read())
        
    asyncio.create_task(init_file(file_name_data, file.size))
    
    return {"filename": file.filename}



