# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

# 这个表单都是有问题的，现在不写登录相关的

class LoginForm(Form):
    """登录用户表单
    """
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])


class RegisterForm(Form):
    """注册用户表单
    """
    username = TextField(u'用户名', validators = [
        validators.Required(message=u'用户名不能为空')
    ])
    password = PasswordField(u'密码', [
        validators.Required(message=u'密码不能为空')
    ])
    confirm = PasswordField(u'确认密码', [
        validators.EqualTo('password', message=u'两次输入的密码不一致')
    ])
    email = TextField(u'邮箱', validators = [
        validators.Required(message=u'邮箱不能为空')
    ])
# -*- coding:utf-8 -*-

class SettingForm(Form):
    """修改用户信息表单
    """
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    email = TextField('email', validators = [Required()])