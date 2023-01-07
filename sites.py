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
import re
from email.message import EmailMessage
import ssl
import smtplib
import random



def convertTuple(tup):
  if tup is not None:
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

def CheckEmail(EmailA):
  regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

  if(re.fullmatch(regex, EmailA)):
    print("Valid Email")
    return True
  else:
    print("Invalid Email")
    return False

def SRcode():
  code = random.randint(1000,9999)
  return code

def sendEC(user_token, code):
  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()
  EmailA = c.execute(f"SELECT Email FROM profiles WHERE Token = '{user_token}';")
  EmailA = c.fetchone()
  EmailA = convertTuple(EmailA)
  email_sender = 'nikitaapp03102023@gmail.com'
  email_password = os.environ['nikitaapp03102023@gmail.com']
  email_receiver = EmailA
    
  subject = 'Verify you Email'
  body = f"""
  verivication code is {code}
  """

  em = EmailMessage()

  em['From'] = email_sender
  em['To'] = email_receiver
  em['Subject'] = subject
  em.set_content(body)

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
  
  c.execute(f"UPDATE profiles SET lastEvcode = '{code}' WHERE Token = '{user_token}';") 
  
  conn.commit()
  conn.close()


os.system('cls')

app = Flask(__name__)


@app.route("/")
def index():
  return render_template('index.html')


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
  if result_UN != None:
    return result_UN
  else:
    return "error 404"


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
  if result_RM != None:
    return result_RM
  else:
    return "error 404"


@app.route("/SignUp")
def signup():
  return render_template('signup.html')


@app.route("/register")
def register():
  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()

  username = request.args.get('username', type = str)
  password = request.args.get('password', type = str)
  Email = request.args.get('Email', type = str)
  rand_token = str(uuid4())
  Read_me = "Hello World!"
  Ev = "No"

  checkUsername = c.execute(f"SELECT username FROM profiles WHERE username = '{username}';")
  checkUsername = c.fetchone()

  if checkUsername == None:
    if CheckEmail(Email) == True:
      checkEmail = c.execute(f"SELECT Email FROM profiles WHERE Email = '{Email}';")
      checkEmail = c.fetchone()
      if checkEmail == None:
        values = (username, Email, Ev, password, rand_token, Read_me)
        c.execute("INSERT INTO profiles VALUES (null, ?, ?, ?, ?, ?, ?, null)", values)
        conn.commit()
        conn.close()
        return rand_token
      else:
        conn.close()
        return "Email is Used."
    else:
      conn.close()
      return "Email is Invalid."
  else:
    conn.close()
    return "You already have an account."


@app.route("/Vemail")
def SendEvcode():
  return render_template('VEmail.html')

  
@app.route("/SendEVcode")
def SendEVcode():
  user_token = request.args.get('userT', type = str)
  Code = random.randint(1000,9999)
  sendEC(user_token, Code)
  return "Sent"
  

@app.route("/checkEVcode")
def checkEVcode():
  conn = sqlite3.connect('DB/profiles.db', check_same_thread=False)
  c = conn.cursor()
  user_token = request.args.get('userT', type = str)
  Evcodev = request.args.get('Evcodev', type = str)
  EvCode = c.execute(f"SELECT lastEvcode FROM profiles WHERE Token = '{user_token}';")
  EvCode = c.fetchone()
  Ev = "Yes"
  res=""
  for i in EvCode:
    res+=str(i)
  res=int(res)
  EvCode = res
  print(EvCode)
  print(Evcodev)
  if str(EvCode) == str(Evcodev):
    c.execute(f"UPDATE profiles SET EmailVerified = '{Ev}' WHERE Token = '{user_token}';") 
    conn.commit()
    conn.close()
    return "True"
  else:
    conn.close()
    return "False"

    

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
def profile():
  return render_template('profile.html')


@app.route("/editprofile")
def editprofile():
  return render_template('Editprofile.html')


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


IID = True
print(IID)

if IID == False:
  hostname=socket.gethostname()  
  IPAddr=socket.gethostbyname(hostname)  
  app.run(host=IPAddr)
elif IID == True:
  app.run(port=8080, debug=True)
else:
    port = int(os.environ.get('PORT', 1000))
    app.run(host='0.0.0.0', port=port)