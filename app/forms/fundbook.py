# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class FundbookForm(Form):

    project_code = StringField(u'项目代码')
    principal = StringField(u'负责人')
    total_amount = StringField(u'经费总额')
