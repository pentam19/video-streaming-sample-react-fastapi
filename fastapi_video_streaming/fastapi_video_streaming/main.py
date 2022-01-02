from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from os import path
import os
from typing import Optional

app = FastAPI()

templates = Jinja2Templates(directory="./fastapi_video_streaming/templates")
video_file_path = "./fastapi_video_streaming/sample.mp4"
#video_file_path = "./fastapi_video_streaming/free.mp4"
# ffmpeg -i sample.mp4 -codec copy -movflags faststart sample2.mp4
#video_file_path = "./fastapi_video_streaming/sample2.mp4"


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/video")
def video():
    def iterfile():  # (1)
        with open(video_file_path, mode="rb") as file_like:  # (2)
            yield from file_like  # (3)

    return StreamingResponse(iterfile(), media_type="video/mp4")


CONTENT_CHUNK_SIZE = 100*1024


@app.get("/stream")
async def stream(range: Optional[str] = Header(None)):
    def get_file():
        f = open(video_file_path, 'rb')
        return f, os.path.getsize(video_file_path)

    def chunk_generator_from_stream(stream, chunk_size, start, size):
        bytes_read = 0
        stream.seek(start)
        while bytes_read < size:
            bytes_to_read = min(chunk_size, size - bytes_read)
            yield stream.read(bytes_to_read)
            bytes_read = bytes_read + bytes_to_read
        stream.close()

    asked = range or "bytes=0-"
    print(asked)
    stream, total_size = get_file()
    start_byte = int(asked.split("=")[-1].split('-')[0])

    return StreamingResponse(
        chunk_generator_from_stream(
            stream,
            start=start_byte,
            chunk_size=CONTENT_CHUNK_SIZE,
            size=total_size
        ), headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start_byte}-{start_byte+CONTENT_CHUNK_SIZE}/{total_size}",
            "Content-Type": "video/mp4"
        },
        status_code=206)
