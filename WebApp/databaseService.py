import psycopg2
from flask import Flask, render_template, redirect, url_for, request, session
import json

app = Flask(__name__)

def connection():
   conn = psycopg2.connect(user="",
                                  password="",
                                  host="",
                                  port="",
                                  database="")

   c = conn.cursor()

   return c, conn

@app.route("/loanApplicationToDB", methods=['GET','POST'])
def loanApplicationToDB():
    data = json.loads(request.data)
    loanamount = data['loanamount']
    interestrate = data['interestrate']
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    c, conn = connection()
    c.execute("INSERT INTO accinfo (loanamount, interestrate, firstname, lastname, email) VALUES (%s, %s, %s, %s, %s)",
              (loanamount, interestrate, firstname, lastname, email))
    conn.commit()
    c.close()
    conn.close()
    return {}

@app.route("/getResults", methods=['POST'])
def getResults():
    c, conn = connection()
    c.execute("SELECT * FROM accinfo")
    content = c.fetchall()
    c.close()
    conn.close()
    d = dict()
    d['data'] = content
    return d

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port="3738")
