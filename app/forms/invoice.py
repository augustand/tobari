# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField, FileField, DecimalField, DateTimeField, SelectField
from wtforms.validators import DataRequired, regexp
from app.models.Subject import Subject


class InvoiceForm(Form):
    """发票信息
    
    其他和发票有关的表单都放在这个文件中
    注意，新版本的 WTForm 用 StringField 替代了 TextField，其他变化和 API 请查阅文档
    """
    subject_id = SelectField(u'科目', coerce=int)
    picture = FileField(u'照片')
    amount = DecimalField(u'发票金额', validators=[DataRequired()])
#     account_id = IntegerField(u'账单号')
    invoice_date = DateTimeField(u'发票票面日期', format='%Y-%m-%d')
    description = StringField(u'发票汇总内容')
    detail = StringField(u'发票内容明细')
    is_consumed = BooleanField(u'是否为未消费的票')
