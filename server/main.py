from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

import cv2


app = FastAPI()



app.mount("/css", StaticFiles(directory="../web/css/"), name="css")
app.mount("/html", StaticFiles(directory="../web/html/"), name="html")
app.mount("/js", StaticFiles(directory="../web/js/"), name="js")

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("../web/html/index.html", "r") as file:
            html_content = file.read()
            return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="found")
    
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/video/")
async def streamer(response: Response):
    print("streaming")

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
    