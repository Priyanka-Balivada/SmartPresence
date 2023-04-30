import cv2
import pyzbar.pyzbar as pyzbar
import pyqrcode
from pyzbar.pyzbar import ZBarSymbol
import streamlit as st
import mysql.connector
import pandas as pd
import urllib.request as request
from bs4 import BeautifulSoup as bs
import re
import json
import time
import datetime;


count=0;
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def decode(im):
    decoded_objs = pyzbar.decode(im, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])

    for obj in decoded_objs:
        return obj.data.decode('utf-8')

def scan():
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    prev_data = None 
    with placeholder.container():
        st.title("SmartPresence")
        st.subheader("Scan the Temperature and QR Code")

        col1, col2, col3, col4, col5 = st.columns([5,10,5,5,5])
       
    
        with col1:
            st.header("PRN")
        with col2:
            st.header("Name")
        with col3:
            st.header("Div")
        with col4:
            st.header("Temp")
        with col5:
            st.header("Time")

            rows = run_query("SELECT * FROM roboracing;")
            for row in rows:
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(f"{row[3]}")
                        with col5:
                            st.write(row[4].strftime("%H:%M:%S"))

        while True:
            TS = request.urlopen("http://api.thingspeak.com/channels/2108652/feeds/last.json?api_key="+st.secrets["api_key"]);
            response = TS.read()
            datawebsite=json.loads(response)

            object = float(datawebsite['field2']) 

            ret, frame = cap.read()

            data = decode(frame)

            if data is not None and data != prev_data:
                prev_data = data
                rows = run_query("SELECT student.PRN, student.name, student.division FROM student where PRN="+data+";")
                for row in rows:
                        timevar = datetime.datetime.now()
                        with col1:
                            st.write(f"{row[0]}")
                        with col2:
                            st.write(f"{row[1]}")
                        with col3:
                            st.write(f"{row[2]}")
                        with col4:
                            st.write(object)
                        with col5:
                            st.write(timevar.strftime("%H:%M:%S"))

                        query="INSERT INTO roboracing values(%s,%s,%s,%s,%s)";
                        val = (str(row[0]), str(row[1]), str(row[2]),str(object),str(timevar));
                        cursor=conn.cursor()
                        cursor.execute(query, val);
                        conn.commit();

            cv2.imshow('QRCode Scanner', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

placeholder = st.empty()

if __name__ == '__main__':
        with placeholder.container():
            user=st.text_input("Username")
            passwd=st.text_input("Password")
            if st.button("Login"):
                if((user=="Admin" ) and (passwd=="123")):
                    scan()
