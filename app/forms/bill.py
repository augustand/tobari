# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, regexp


class BillForm(Form):
    """账单信息
    
    其他和发票有关的表单都放在这个文件中
    注意，新版本的 WTForm 用 StringField 替代了 TextField，其他变化和 API 请查阅文档
    """
    bank = StringField(u'账单所属银行')
    html_file = FileField(u'HTML文件')
    