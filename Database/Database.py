from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import requests

class InfluxDataBase:
    
    def __init__(self,server_URL,token,org) -> None:
        self.client=InfluxDBClient(server_URL, token=token, org=org)
        self.write_api=self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api=self.client.query_api()
        self.server_URL=server_URL
        self.token=token
        self.org=org

    def write_data(self,data) -> None:
        executable_code='Point(data.measurement)'
        n_fields=len(data.field)
        n_tag=len(data.tag)
        for i in range(n_tag):
            executable_code=executable_code+'.tag(list(data.tag.keys())[{}],list(data.tag.values())[{}])'.format(i,i)
        for i in range(n_fields):
            executable_code=executable_code+'.field(list(data.field.keys())[{}],list(data.field.values())[{}])'.format(i,i)
        if data.timestamp is not None:
            executable_code=executable_code+'.time(data.timestamp)'

        Data=eval(executable_code)
        self.write_api.write(bucket=data.bucket_name, record=Data)
    
    def read_data(self,data):
        query = f'''
        from(bucket: "{data.bucket_name}")'''+ ''' 
        |> range(start: -{}h, stop: now())'''.format(data.time_interval)+f'''
        |> filter(fn:(r) => r["_measurement"] == "{data.measureament_name}")'''
        for i in range(len(data.tag)):
            query=query+f'''|> filter(fn:(r) => r["{list(data.tag.keys())[i]}"] == "{list(data.tag.values())[i]}") '''
        for i in range(len(data.field)):
            query=query+f'''|> filter(fn:(r) => r["_field"] == "{data.field[i]}") '''
        result = self.query_api.query(org=self.org, query=query) 
        results={}
        for table in result:
            for record in table.records:
                results[record.get_field()]=record.get_value()
        json_result=json.dumps(results)
        return json_result



        
    