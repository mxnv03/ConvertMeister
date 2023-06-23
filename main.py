from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from load import uploading, download
from db import get_filenames, users_files

app = FastAPI()


@app.post("/upload/{nickname}")
async def upload_file(nickname: str, file: UploadFile = File(...)):
    return uploading(file, bucket='upload', nickname=nickname)


@app.get("/download/{nickname}/{filename}")
async def download_file(nickname: str, filename: str):
    return download(nickname, filename)


@app.get("/show/{nickname}")
async def show_users_files(nickname: str):
    return users_files(nickname)


@app.get("/check/{table}")
async def checking(table: str):
    return get_filenames(table)
