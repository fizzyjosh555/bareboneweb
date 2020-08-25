from flask import Flask, render_template, redirect, url_for, request, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

class RegistrationForm(Form):
    firstname = StringField('FirstName', [validators.Length(min=2, max=20)])
    lastname = StringField('LastName', [validators.Length(min=3, max=15)])
    email = StringField('Email', [validators.Length(min=3, max=20)])
    loanamount = StringField('LoanAmount', [validators.Length(min=0, max=20)])
    interestrate = StringField('InterestRate', [validators.Length(min=0, max=15)])

def make_post(url, args):
    result = requests.post(url=url, data=json.dumps(args))
    return result.json()

@app.route('/registration', methods=['GET','POST'])
def registration():
    url = "http://127.0.0.1:3738/loanApplicationToDB"
    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        args = dict()
        args['loanamount'] = form.loanamount.data
        args['interestrate'] = form.interestrate.data
        args['firstname'] = form.firstname.data
        args['lastname'] = form.lastname.data
        args['email'] = form.email.data
        make_post(url, args)

        return redirect(url_for('welcome'))
    return render_template('registration.html', error=error)

@app.route('/matches')
def getMatches():
    url = "http://127.0.0.1:3738/getResults"
    args = dict()
    content = make_post(url, args)['data']
    return render_template('matches.html', content=content)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')