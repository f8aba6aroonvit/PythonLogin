from flask import Flask,jsonify,make_response,request
# from flask_cors import CORS 
from flask_mysqldb import MySQL
import json
import mysql.connector
import pymysql
import jwt
import datetime
from datetime import timedelta
import re

app = Flask(__name__)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # ตั้งค่าเวลาหมดอายุของ Access Token
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  
app.config['SECRET_KEY'] = 'asjdakdsfasasgdagdastdahdrvwq6dyw26347273hsdvdfsr4y23ytg34gf'
# CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_login'
 
db = MySQL(app)


print("dkfjgjsdkfdsjfksflksfj",db)


@app.route("/api/user",methods=['GET'])
def read():
    try:
        cursor = db.connection.cursor()
        sql = "SELECT*FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        print("osdfkldf",result)
        user_list = []
        
        for user in result:
            user_dict = {
                "id": user[0],
                "username": user[1],
                "email": user[3],
                "role":user[5]
            }
            user_list.append(user_dict)

        return jsonify({'users': user_list})
    
    except:
        return "หนังหมาไอ้สัส"


@app.route("/api/user/register",methods=['POST'])
def register():
    email_regex = re.compile(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    tel = request.json.get('tel')
    role = request.json.get('role')
    try:
        sql = "SELECT * FROM users WHERE username = %s OR email = %s"
        cursor = db.connection.cursor()
        cursor.execute(sql, (username, email))
        result = cursor.fetchone()

        if not request.json.get('username') or not request.json.get('password') :
            return jsonify({'message': 'กรุณรากรอกข้อมูลให้ครบ'}), 401

        if not email_regex.match(email):
            return jsonify({'message': 'กรอก Email ให้ถูก Format'})

        
        if result:
            return jsonify({'message': 'มีผู้ใช้ในระบบแล้ว'})

        else :
            sql = "INSERT INTO users (username, password, email,tel,role) VALUES (%s, %s, %s,%s,%s)"
            cursor.execute(sql, (username, password,email,tel,role))
            db.connection.commit()
            return jsonify({'message': 'สร้างสำเร็จ'})
            
    except:
        return "หนังหมาไอ้สัส"
       
   
@app.route("/api/user/login",methods=['POST'])
def login():
    auth = request.json

    try:
        if not auth or not auth.get('username') or not auth.get('password'):
            return jsonify({'message': 'กรุณรากรอกข้อมูลให้ครบ'}), 401
        username = auth.get('username')
        password = auth.get('password')
        role = auth.get('role')

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor = db.connection.cursor()
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        if user:
            token = jwt.encode({
                'role': user[5],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'role':user[5],
            'token': token})

    except:
        return "หนังหมาไอ้สัส"




    








if __name__ =="__main__":
    app.run(debug=True)
