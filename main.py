from fastapi import FastAPI
import requests
from pydantic import BaseModel

app = FastAPI()

class Ex_id(BaseModel):
    ex_id: int
    

@app.post('/')
def stick_video_generator(ex_id:Ex_id):
    headers = {'APP-VERSION': '2',
               "Authorization": 'Bearer  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTcsImVtYWlsIjoiYW1hbnA3OTUyKzk5QGdtYWlsLmNvbSIsInB1YmxpY0FkZHJlc3MiOiIweGZCQjBGNkNFODk2YWQ1Q0JhOGMxQzUzRmUxQkQ5RjZiMjVEQjliMTAiLCJyb2xlIjoidXNlciIsImlhdCI6MTY3MjA2NTE4OCwiZXhwIjoxNjcyMDY1MjQ4fQ.lxApKIuL3UmM_xw3PXXcjn7J6uonV4DOEk1v9MW_JSQ'}
    res = requests.get(f"http://api-stage.sportyapp.gg/exercises/{ex_id.ex_id}")
    datastream = res.json()
    print(datastream)
    return "aman"