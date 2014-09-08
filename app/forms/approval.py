# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField, FileField, DecimalField, DateTimeField, SelectField
from wtforms.validators import DataRequired, regexp


class ApprovalForm(Form):
    """审批单信息
    
    其他和发票有关的表单都放在这个文件中
    注意，新版本的 WTForm 用 StringField 替代了 TextField，其他变化和 API 请查阅文档
    """
    cost_type = SelectField(u'消费类型', coerce=int)
    agent = StringField(u'经办人')
    payee = StringField(u'收款人')
    subject = SelectField(u'科目', coerce=int)
    max_money = DecimalField(u'期望最大金额数')
#     picture = FileField(u'照片')
#     fund_id = IntegerField(u'经费本ID', validators=[DataRequired()])
#     invoice_count = IntegerField(u'发票张数')
#     payee = StringField(u'收款人')
#     subject_list = StringField(u'科目列表')
#     status = SelectField(u'上报状态')
    