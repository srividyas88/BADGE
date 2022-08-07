# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:20:35 2022

@author: USER
"""
from flask import Flask,render_template,request,url_for
import sqlite3
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploadBadge/' ,methods=('GET', 'POST'))
def uploadBadge():
    return render_template('uploadBadge.html')

@app.route('/badge/' ,methods=('GET', 'POST'))
def badge():
    #file = open(r'C:/Users/USER/Desktop/BADGE/badge_start.py', 'r').read()
    #exec(file)
    if request.method == 'POST' :
        try:
            badgeName = request.form['badgeName']
            desc = request.form['desc']
            image=request.form['img']
            elgStudents =request.form['elgStudents']
            conn = sqlite3.connect('test.db')
            
            
        
            print ("Opened database successfully")
            conn.execute('''CREATE TABLE IF NOT EXISTS BADGE
                     (NAME  VARCHAR2(100) PRIMARY KEY     NOT NULL,
                     DESCRIPTION           TEXT   ,
                     IMAGE            TEXT,
                     ELIGIBLE_STUDENTS        CHAR(5000));''')
            print ("Table created successfully")
        except:
            conn.rollback()
            msg = "error in table creation"
            return render_template('badge.html',rows=msg)
            
        try:
            cur = conn.cursor() 
            cur.execute("select * from badge where name =?",(badgeName,))
            nameCount = cur.fetchall()
            for i in nameCount:
                 elgStudents = i[3]+','+elgStudents
            if len(nameCount)>0 :
                cur.execute("UPDATE badge set eligible_students=? where name=?",(elgStudents,badgeName))
                msg = "Record successfully updated" 
            else:
                cur.execute("INSERT INTO badge VALUES (?,?,?,?)",(badgeName,desc,image,elgStudents) )
                msg = "Record successfully added" 
            conn.commit()
            
        except:
            conn.rollback()
            msg = "error in insert operation"
            return render_template('badge.html',rows=msg)
            
        try: 
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("select * from badge")
            msg = cur.fetchall() 
        except:
            conn.rollback()
            conn.close()
    return render_template('badge.html',rows=msg)

@app.route('/verifyBadge/',methods=('GET', 'POST')) 
def verifyBadge():
    return render_template('verifyBadge.html') 


@app.route('/badgeEligibility/' ,methods=('GET', 'POST'))
def badgeEligibility():
    
    if request.method == 'POST' :
        try:
            badgeName = request.form['badgeName']
            email =request.form['email']
            conn = sqlite3.connect('test.db')
            cur = conn.cursor() 
            cur.execute("select * from badge where name =? and eligible_students like ?",(badgeName,'%'+email+'%'))
            nameCount = cur.fetchall()
            if len(nameCount)>0 :
                return render_template('badgeEligibility.html',msg="Student eligible for badge : "+badgeName)
            else:
                return render_template('badgeEligibility.html',msg="Student not eligible for badge : "+badgeName)
        except:
            conn.close()
        
if __name__ == '__main__':
    app.run(debug=True) 