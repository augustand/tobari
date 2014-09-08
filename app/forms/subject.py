# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SelectField,validators,TextField
from wtforms.validators import DataRequired
from app.models.Person import Person

class SubjectForm(Form):
    name = StringField(u'科目名', validators=[])
    description = TextField(u'描述',  validators=[])