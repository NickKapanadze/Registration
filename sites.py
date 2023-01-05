from flask import Flask, render_template, make_response
from flask import Flask
import sqlite3
import json
from flask import Flask, render_template, request
import os
import uuid
from uuid import uuid4
import random
import socket 

def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str

def convert(list):
     
    # Converting integer list to string list
    s = [str(i) for i in list]
     
    # Join list items using join()
    res = int("".join(s))
     
    return(res)

os.system('cls')

app = Flask(__name__)


@app.route("/")
def index():
  return render_template('index.html')
  app.config['SERVER_NAME'] = website_url


@app.route("/get2")
def getfromdatabase():
  conn = sqlite3.connect('DB/profiles.db')
  c = conn.cursor()

  results = []
  for row in c.execute("SELECT Username, ReadMe FROM profiles"):
    results.append(row)


  conn.close()
  return json.dumps(results)


@app.route("/get")
def getfromdatabase2():
  return render_template('list.html')


@app.route("/getCC")
def getIfroDB():
  conn = sqlite3.connect('DB/profiles.db')
  c = conn.cursor()

  Ccount = c.execute(f"SELECT COUNT(*) FROM profiles;")
  Ccount = c.fetchone()
  Ccount = convert(Ccount)
  print(Ccount)
  conn.close()
  return json.dumps(Ccount)


@app.route("/GetB_N")
def fromdatabase3N():
  conn = sqlite3.connect('DB/profiles.db')
  c = conn.cursor()
  U_id = request.args.get('U_ID', type = str)
  result_UN = c.execute(f"SELECT Username FROM profiles WHERE AccountID = {U_id};")
  result_UN = c.fetchone()
  result_UN = convertTuple(result_UN)
  print(result_UN, U_id)
  conn.close()
  return result_UN


@app.route("/GetB_RM")
def fromdatabase3RM():
  conn = sqlite3.connect('DB/profiles.db')
  c = conn.cursor()
  U_id = request.args.get('U_ID', type = str)
  result_RM = c.execute(f"SELECT ReadMe FROM profiles WHERE AccountID = {U_id};")
  result_RM = c.fetchone()
  result_RM = convertTuple(result_RM)
  print(result_RM, U_id)
  conn.close()
  return result_RM


@app.route("/SignUp")
def signup():
  return render_template('signup.html')


@app.route("/register")
def register():
  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()

  username = request.args.get('username', type = str)
  password = request.args.get('password', type = str)
  rand_token = str(uuid4())
  Read_me = "Hello World!"

  checkUsername = c.execute(f"SELECT username FROM profiles WHERE username = '{username}';")
  checkUsername = c.fetchone()

  print(username)
  print(password)
  print(checkUsername)
  print(rand_token)

  values = (username, password, rand_token, Read_me)

  if checkUsername == None:
    c.execute("INSERT INTO profiles VALUES (null, ?, ?, ?, ?)", values)

    conn.commit()
    conn.close()
    return rand_token
  else:
    conn.close()
    return "You already have an account."
    

@app.route("/LogIn")
def LogIn():
  return render_template('login.html')


@app.route("/LogInC")
def LogInC():
  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()

  username = request.args.get('Username', type = str)
  password = request.args.get('Password', type = str)

  checkUsername = c.execute(f"SELECT username FROM profiles WHERE username = '{username}';")
  checkUsername = c.fetchone()

  if checkUsername == None:
    conn.close()
    return "U is wrong"
  else:
    checkPassword = c.execute(f"SELECT Password FROM profiles WHERE username = '{username}';")
    checkPassword = str(c.fetchone()[0]) 
    if checkPassword == password:
      ReadT = c.execute(f"SELECT Token FROM profiles WHERE username = '{username}';")
      ReadT = str(c.fetchone()[0]) 
      conn.close()
      return ReadT
    else:
      conn.close()
      return "P is wrong"


@app.route("/profile")
def profiles():

  return render_template('profile.html')


@app.route("/readname")
def readname():
  
  user_token = request.args.get('userT', type = str)
  
  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()

  username = c.execute(f"SELECT username FROM profiles WHERE Token = '{user_token}';")
  username = c.fetchone()
  username = convertTuple(username)
  
  print(user_token)
  print(username)

  conn.close()

  result = username
  result = str(result)
  return result

  
@app.route("/readreadme")
def readreadme():

  user_token = request.args.get('userT', type = str)

  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()

  Read_me = c.execute(f"SELECT ReadMe FROM profiles WHERE Token = '{user_token}';")
  Read_me = c.fetchone()
  Read_me = convertTuple(Read_me)

  print(user_token)
  print(Read_me)
  
  conn.close()

  result = Read_me
  result = str(result)
  return result


@app.route("/updatereadme")
def updatereadme():
  nRM = request.args.get('nRM', type = str)
  user_token = request.args.get('userT', type = str)

  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()

  print(user_token)
  print(nRM)

  c.execute(f"UPDATE profiles SET ReadMe = '{nRM}' WHERE Token = '{user_token}';") 
  
  conn.commit()
  conn.close()
  return "done!"


IID = False
print(IID)

if IID == False:
  hostname=socket.gethostname()  
  IPAddr=socket.gethostbyname(hostname)  
  app.run(host=IPAddr)
elif IID == True:
  app.run(port=8080, debug=True)
else:
  app.run(host = '0.0.0.0')