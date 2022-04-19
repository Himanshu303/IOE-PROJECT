from functools import wraps
import sys
import os
import pickle
import pandas as pd
import joblib
from flask import Flask, render_template, redirect, request, url_for, session
#coming from pyrebase4
import pyrebase

config = {
                "apiKey": "AIzaSyCafYESgXTjTbP7y4mkCQdlQLuXgif71vA",
                "authDomain": "weathermonitoring-4ca0f.firebaseapp.com",
                "databaseURL": "https://weathermonitoring-4ca0f-default-rtdb.firebaseio.com",
                "projectId": "weathermonitoring-4ca0f",
                "storageBucket": "weathermonitoring-4ca0f.appspot.com",
                "messagingSenderId": "378902356907",
                "appId": "1:378902356907:web:bbda4726ab23051f8ca8ee",
                "measurementId": "G-M464N5Y7WW"
            }

firebase = pyrebase.initialize_app(config)
#auth instance
auth = firebase.auth()
#real time database instance
db = firebase.database();


app = Flask(__name__)
#secret key for the session
app.secret_key = os.urandom(24)


@app.route("/record")
def record():
    temp = db.child("Temperature").get()
    hum= db.child("Humidity").get()
    moist = db.child("Moisture").get()
    dt = db.child("DateTime").get()
    
    temperature=[]
    for i in temp:
        if i:
         temperature.append(i.val())

    moisture=[]
    for i in moist:
         if i:
          moisture.append(i.val())

    humidity=[]
    for i in hum:
         if i:
          humidity.append(i.val())

    date=[]
    for i in dt:
         if i:
          date.append(i.val())
  
    print(temperature)
    print(moisture)
    print(humidity)
    print(date)
    length=min(len(temperature),len(humidity),len(moisture),len(date))
    temperature=temperature[::-1]
    moisture=moisture[::-1]
    humidity=humidity[::-1]
    date=date[::-1]

    if temp.val() == None or hum.val()==None or moist.val()==None or dt.val()==None:
     
      return render_template("record.html")
    else:
      return render_template("record.html", temperature=temperature, moisture=moisture, humidity=humidity, date=date,length=length)

@app.route("/")
def index():
    temp = db.child("Temperature").get()
    hum= db.child("Humidity").get()
    moist = db.child("Moisture").get()
    dt = db.child("DateTime").get()
    
    temperature=[]
    for i in temp:
        if i:
         temperature.append(i.val())

    moisture=[]
    for i in moist:
         if i:
          moisture.append(i.val())

    humidity=[]
    for i in hum:
         if i:
          humidity.append(i.val())

    date=[]
    for i in dt:
         if i:
          date.append(i.val())

    temperature=temperature[::-1]
    moisture=moisture[::-1]
    humidity=humidity[::-1]
    date=date[::-1]

    temp_av,moist_av,humi_av=0,0,0
    for i in range(len(temperature)):
        temp_av+=float(temperature[i])
    for i in range(len(moisture)):
        moist_av+=float(moisture[i])
    for i in range(len(humidity)):     
        humi_av+=float(humidity[i])
   
    temp_av/=len(temperature)
    moist_av/=len(moisture)
    humi_av/=len(humidity)
    cmip=((float(moisture[0])/1024)*100)-100
    amip=((float(moist_av)/1024)*100)-100.0

    temp_av=(round(temp_av, 2))
    humi_av=(round(humi_av, 2))
    moist_av=(round(moist_av, 2))
    regr3 = joblib.load('filename.pkl')
    tp=[[temp_av,humi_av]]
    tp=pd.DataFrame(tp,columns=["Temperature","Humidity"])
    
    n=regr3.predict(tp)
    val1=n.tolist()
    maxi=max(max(val1))
    val2=[]
    for i in range(5):
     val2.append(val1[0][i])
    print(val2)
    val3=val2.index(maxi)

    if val3==0:
     Maincrop="Corn"
     corn=1
     potato=0
     rice=0
     soyabean=0
     wheat=0
    elif val3==1:
     Maincrop="Potato"
     corn=0
     potato=1
     rice=0
     soyabean=0
     wheat=0
    elif val3==2:
     Maincrop="Rice"
     corn=0
     potato=0
     rice=1
     soyabean=0
     wheat=0
    elif val3==3:
     Maincrop="Soyabean"
     corn=0
     potato=0
     rice=0
     soyabean=1
     wheat=0
    elif val3==4:
     Maincrop="Wheat"
     corn=0
     potato=0
     rice=0
     soyabean=0
     wheat=1

     
    alert=0
    if cmip>50:
        alert=1



      



    if temp.val() == None or hum.val()==None or moist.val()==None or dt.val()==None:  
      return render_template("index.html")
    else:
      return render_template("index.html", temperature=temperature, moisture=moisture, humidity=humidity, date=date,temp_av=temp_av,moist_av=moist_av,humi_av=humi_av,Maincrop=Maincrop,cmip=cmip,amip=amip,alert=alert,rice=rice,wheat=wheat,soyabean=soyabean,corn=corn,potato=potato)

@app.route("/currentprediction")
def currentprediction():
    temp = db.child("Temperature").get()
    hum= db.child("Humidity").get()
    moist = db.child("Moisture").get()
    dt = db.child("DateTime").get()
    
    temperature=[]
    for i in temp:
        if i:
         temperature.append(i.val())

    moisture=[]
    for i in moist:
         if i:
          moisture.append(i.val())

    humidity=[]
    for i in hum:
         if i:
          humidity.append(i.val())

    date=[]
    for i in dt:
         if i:
          date.append(i.val())

    temperature=temperature[::-1]
    moisture=moisture[::-1]
    humidity=humidity[::-1]
    date=date[::-1]

    cmip=((float(moisture[0])/1024)*100)-100.0

    regr3 = joblib.load('filename.pkl')
    tp=[[temperature[0],humidity[0]]]
    tp=pd.DataFrame(tp,columns=["Temperature","Humidity"])
    
    n=regr3.predict(tp)
    val1=n.tolist()
    maxi=max(max(val1))
    val2=[]
    for i in range(5):
     val2.append(val1[0][i])
    print(val2)
    val3=val2.index(maxi)

    if val3==0:
     Maincrop="Corn"
     corn=1
     potato=0
     rice=0
     soyabean=0
     wheat=0
    elif val3==1:
     Maincrop="Potato"
     corn=0
     potato=1
     rice=0
     soyabean=0
     wheat=0
    elif val3==2:
     Maincrop="Rice"
     corn=0
     potato=0
     rice=1
     soyabean=0
     wheat=0
    elif val3==3:
     Maincrop="Soyabean"
     corn=0
     potato=0
     rice=0
     soyabean=1
     wheat=0
    elif val3==4:
     Maincrop="Wheat"
     corn=0
     potato=0
     rice=0
     soyabean=0
     wheat=1


     
    alert=0
    if cmip<50:
        alert=1




    if temp.val() == None or hum.val()==None or moist.val()==None or dt.val()==None:  
      return render_template("currentprediction.html")
    else:
      return render_template("currentprediction.html", temperature=temperature, moisture=moisture, humidity=humidity, date=date,Maincrop=Maincrop,cmip=cmip,alert=alert,rice=rice,wheat=wheat,soyabean=soyabean,corn=corn,potato=potato)



#run the main script
if __name__ == "__main__":
    app.run(debug=True)