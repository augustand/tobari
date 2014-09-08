# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, validators, IntegerField, BooleanField, FileField, TextAreaField
from wtforms.validators import DataRequired
from app.models.Invoice import Invoice
import re


class Invoice_Picture_Form(Form):
    picture = FileField(u'发票照片')  # , [validators.regexp(u'^[^/\\]\.jpg$')]
#     description = TextAreaField(u'Image Description')

    def validate_image(self, form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
