from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import model
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import cv2
from detection import detection

detector = detection()
app = FastAPI()



model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class stream_data(BaseModel):
    url: str
    location: str
    date: str



app.mount("/css", StaticFiles(directory="../web/css/"), name="css")
app.mount("/html", StaticFiles(directory="../web/html/"), name="html")
app.mount("/js", StaticFiles(directory="../web/js/"), name="js")


@app.get("/", response_class=HTMLResponse)
async def root(db: Session = Depends(get_db)):

    try:
        with open("../web/html/index.html", "r") as file:
            html_content = file.read()
            return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="found")




def generate_frames(video_path):
    camera = cv2.VideoCapture(video_path)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            boxes, scores, classe = detector.predict(frame)
            frame = detector.visual(frame, boxes, classe, scores)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

url_list = []

@app.get("/video/{stream_id}")
async def streamer(stream_id:int, db: Session = Depends(get_db)):
    streams = db.query(model.Stream).all()
    for stream in streams:
        url_list.append(stream.url)


    return StreamingResponse(generate_frames(url_list[stream_id]), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/streams")
async def get_streams(db: Session = Depends(get_db)):
    streams = db.query(model.Stream).all()
    return streams


@app.get("/stream_number")
async def get_number(db: Session = Depends(get_db)):
    streams = db.query(model.Stream).all()
    return len(streams)

@app.post("/streams")
async def create_stream(stream: stream_data, db: Session = Depends(get_db)):
    db_stream = model.Stream()
    db_stream.url = stream.url
    db_stream.location = stream.location
    db_stream.date = stream.date

    db.add(db_stream)
    db.commit()

    return stream

@app.put("/streams/{stream_id}")
async def update_stream(stream_id: int, stream: stream_data, db: Session = Depends(get_db)):
    db_stream = db.query(model.Stream).filter(model.Stream.id == stream_id).first()
    db_stream.url = stream.url
    db_stream.location = stream.location
    db_stream.date = stream.date

    db.add(db_stream)
    db.commit()

    return stream

@app.delete("/streams/{stream_id}")
async def delete_stream(stream_id: int, db: Session = Depends(get_db)):
    db.query(model.Stream).filter(model.Stream.id == stream_id).delete()
    db.commit()

    return {"message": "stream deleted successfully"}