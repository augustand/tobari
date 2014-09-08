# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class FundForm(Form):

    fundbook_id = IntegerField(u'经费本ID')
    income = IntegerField(u'收入')
    expend = IntegerField(u'支出')
    abtract = StringField(u'摘要')
