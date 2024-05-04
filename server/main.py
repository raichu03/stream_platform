from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import model
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import cv2
from detection import detection
import datetime
import requests
import time

## initializes the object detection model
detector = detection()

## starts the web app
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
    lat: float
    long: float
    date: str

class location_data(BaseModel):
    classe: str
    lat: float
    long: float
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


def generate_frames(video_path, lat, long):
    camera = cv2.VideoCapture(video_path)
    
    def call_after_interval(interval_seconds):
        def decorator(func):
            last_called = 0

            def wrapper(*args, **kwargs):
                nonlocal last_called
                current_time = time.time()
                if current_time - last_called >= interval_seconds:
                    last_called = current_time
                    return func(*args, **kwargs)

            return wrapper
        return decorator

    @call_after_interval(300)
    def update_loocation(classe, lat, long, date):
        animals = {
            1: 'boar',
            2: 'buffalo',
            3: 'cow/bull',
            4: 'dog',
            5: 'elephant',
            6: 'leopard',
            7: 'monkey',
            8: 'snake',
            9: 'tiger',
            10: 'other'
        }
        classe = animals[classe]
        requests.post("http://127.0.0.1:8000/locations", json={"classe": classe,"lat": lat, "long": long, "date": date})
        
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            boxes, scores, classe = detector.predict(frame)
            frame = detector.visual(frame, boxes, classe, scores)
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if len(classe) > 0:
                update_loocation(classe[0], lat, long, date)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

url_list = []
lat_list = []
long_list = []

@app.get("/video/{stream_id}")
async def streamer(stream_id:int, db: Session = Depends(get_db)):
    streams = db.query(model.Stream).all()

    for stream in streams:
        url_list.append(stream.url)
        lat_list.append(stream.lat)
        long_list.append(stream.long)


    return StreamingResponse(generate_frames(url_list[stream_id], lat_list[stream_id], long_list[stream_id]), media_type="multipart/x-mixed-replace; boundary=frame")


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
    db_stream.lat = stream.lat
    db_stream.long = stream.long
    db_stream.date = stream.date

    db.add(db_stream)
    db.commit()

    return stream

@app.put("/streams/{stream_id}")
async def update_stream(stream_id: int, stream: stream_data, db: Session = Depends(get_db)):
    db_stream = db.query(model.Stream).filter(model.Stream.id == stream_id).first()
    db_stream.url = stream.url
    db_stream.lat = stream.lat
    db_stream.long = stream.long
    db_stream.date = stream.date

    db.add(db_stream)
    db.commit()

    return stream

@app.delete("/streams/{stream_id}")
async def delete_stream(stream_id: int, db: Session = Depends(get_db)):
    db.query(model.Stream).filter(model.Stream.id == stream_id).delete()
    db.commit()

    return {"message": "stream deleted successfully"}

from sqlalchemy import func
###### return the location of the cameras where object was detected ######
@app.get("/locations")
async def get_locations(db: Session = Depends(get_db)):
    locations = db.query(model.Location).order_by(model.Location.date.desc()).group_by(model.Location.lat, model.Location.long).all()
    return locations

###### add the location of the cameras where object was detected ######
@app.post("/locations")
async def create_location(location: location_data, db: Session = Depends(get_db)):
    db_location = model.Location()
    db_location.classe = location.classe
    db_location.lat = location.lat
    db_location.long = location.long
    db_location.date = location.date

    db.add(db_location)
    db.commit()

    return location