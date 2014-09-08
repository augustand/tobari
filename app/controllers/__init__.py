# -*- coding:utf-8 -*-
import os
import glob

from flask import render_template

from app import app


# from flask_login import login_user
from person import person
from invoice import invoice
from bill import bill
from approval import approval
from picture import picture
from subject import subject
from account import account
from fundbook import fundbook
from fund import fund

__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.dirname(__file__) + "/*.py")]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=u'主页')


@app.route('/hello')
def hello():
    return render_template('hello.html')

# app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(person, url_prefix='/person')
app.register_blueprint(invoice, url_prefix='/invoice')
app.register_blueprint(bill, url_prefix='/bill')
app.register_blueprint(approval, url_prefix='/approval')
app.register_blueprint(fundbook, url_prefix='/fundbook')
app.register_blueprint(picture, url_prefix='/picture')
app.register_blueprint(subject, url_prefix='/subject')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(fund, url_prefix='/fund')
