from fastapi import FastAPI
import uvicorn
from Model.Model import WritingData, ReadingData
from Database.Database import InfluxDataBase
from pydantic import BaseModel
from typing import List

server_URL="http://localhost:8086"
token="ysCdkFn7aP_FpPyxRA9RvMZ5Gkb7bFBTbj-8h5BFJqwcI4Atg5D-i4Ws8ve8H8jLXSzeMiQN9SArj58IC1EYiQ=="
org="6b3bad4e03c1ae1d"
bucket="d51dbef4287e09bf"

Influx = InfluxDataBase(server_URL,token,org)
app = FastAPI()

@app.post('/write/')
async def call_writing_influx(data: WritingData):
    Influx.write_data(data)

@app.post('/read/')
async def call_reading_influx(data: ReadingData):
    return Influx.read_data(data)
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
