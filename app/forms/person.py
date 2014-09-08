# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SelectField,validators
from wtforms.validators import DataRequired
from app.models.Person import Person

class PersonForm(Form):
    """用户个人信息表单
    
    其他和个人有关的表单都放在这个文件中
    注意，新版本的 WTForm 用 StringField 替代了 TextField，其他变化和 API 请查阅文档
    """
    
    name = StringField(u'姓名', validators=[
        DataRequired(message=u'姓名不能为空'),
    ])
    tax_type = SelectField(u'计税身份', choices=Person.get_tax_type())
    office = StringField(u'办公室')
    telephone = StringField(u'手机号码')
    identity_card = StringField(u'身份证号码')
    job_number = StringField(u'工号')
    business_card_id = StringField(u'公务卡')
    debit_card_id = StringField(u'信用卡')
    opening_bank = StringField(u'开户行')
    mobile = StringField(u'电话号码')
    
    