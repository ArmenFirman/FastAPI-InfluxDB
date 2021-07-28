from fastapi import FastAPI
import uvicorn
import yaml
from yaml.loader import SafeLoader
from Model.Model import WritingData, ReadingData
from Database.Database import InfluxDataBase



with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile,Loader=SafeLoader)
server_URL=cfg["InfluxDB"]["server_URL"]
token=cfg["InfluxDB"]["token"]
org=cfg["InfluxDB"]["org"]

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
