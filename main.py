#Impor package
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
import pandas as pd

#Membuat objek FastAPI
app = FastAPI()

#variabel password
password = "123456"




#Membuat endpoint

#Define End point
@app.get("/")
#Function Menghandle end point diatas
def getWelcome():
    return {
        "msg": "Selamat datang di web"
    }
    
#Matiin dengan (control + c) di terminal

#Endpoint menampilkan data set
@app.get("/data")
#Function mengambil data
def getData():
    df = pd.read_csv("dataset.csv")
    return df.to_dict(orient="records")

#Endpoint menampilkan data sesuai lokasi
@app.get("/data/{location}") #location berubah sesuai lokasi
#Function mengambil data
def getData(location: str):
    df = pd.read_csv("dataset.csv")
    #filter
    df_loc = df[df['location']== location]
    
    #validasi
    if len(df_loc) == 0:
        #Menampilkan pesan error
        raise  HTTPException(status_code=404, detail="Data not found")
    return df_loc.to_dict(orient="records")

#Endpoint menghapus id
@app.delete("/data/{id}") 
#Function mengambil data
def delData(id: int, api_key: str = Header(None)):
    #Verifikasi authentication
    if api_key == None or api_key != password:
        raise HTTPException(status_code=401, detail="You don't have acces")
    
    df = pd.read_csv("dataset.csv")
    #filter
    df_id = df[df['id']== id]
    
    #validasi
    if len(df_id) == 0:
        #Menampilkan pesan error
        raise  HTTPException(status_code=404, detail="Data not found")
    
    #proses hapus
    df_id = df[df['id']!= id]
    
    #update csv
    df_id.to_csv('dataset.csv', index=False)
    
    return {
        "msg":"Data berhasil dihapus"
    }


#class untuk data
class Profile(BaseModel):
    id: int
    name: str
    age: int
    location: str

#Endpoint menambah data
@app.post("/data/create") 
#Function mengambil data
def createData(profile: Profile):
    
    #Membaca data
    df = pd.read_csv("dataset.csv")
    
    #Proses menambah data
    
    newData = pd.DataFrame({
    'id' : [profile.id],
    'name' : [profile.name],
    'age': [profile.age],
    'location' : [profile.location],
    'created_at': [datetime.now().date()],  
    })

    
    #concat
    df = pd.concat([df, newData])
    
    #update CSV
    df.to_csv('dataset.csv',index=False)
    
    return {
        "msg": "Data berhasil ditambah"
    }