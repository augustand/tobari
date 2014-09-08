# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField, FileField, DecimalField, DateTimeField, SelectField, TextField,validators
from wtforms.validators import DataRequired, regexp
from app.models.Account import Account


class AccountForm(Form):
    """帐目信息
    
    其他和发票有关的表单都放在这个文件中
    注意，新版本的 WTForm 用 StringField 替代了 TextField，其他变化和 API 请查阅文档
    """
#     bill_id = IntegerField(u'账单编号')
    funder = StringField(u'出资人')
    transaction_money = DecimalField(u'交易金额')
    currency = SelectField(u'币种', choices=Account.get_currencies())
    enter_money = DecimalField(u'入账金额')
    enter_date = DateTimeField(u'记账日', format='%Y-%m-%d')
    card_no = StringField(u'卡号后四位', [validators.length(max=4)])
    trade_abstract = StringField(u'交易摘要')
    transaction_place = StringField(u'交易地点')
    is_submit = BooleanField(u'是否需要报销')
#     status_index = SelectField(u'发票抵冲账单的记录', coerce=int, choices=Account.get_status())
    
