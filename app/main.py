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
    filename = ''.join(file.filename.split('.')[:-1])

    if not os.path.isdir(os.path.join("uploads", filename)):
        os.makedirs(f"uploads/{filename}")
    
    with open(f"uploads/{filename}/{file.filename}", "wb") as f:
        f.write(await file.read())
        
    asyncio.create_task(init_file(file.size, f"uploads/{filename}/{file.filename}",f"uploads/{filename}/{file.filename}"))
    
    return {"filename": file.filename}



