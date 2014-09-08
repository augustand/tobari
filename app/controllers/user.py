# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, g, session, flash, redirect, url_for

from app import app
from app.models.User import User
from app.forms.user_form.login_form import LoginForm
from app.forms.user_form.setting_form import SettingForm
from app.forms.user_form.register_form import RegisterForm


user = Blueprint('user', __name__, template_folder='user')


@app.before_request
def before_request():
    g.user = current_user


@app.route('/register', methods=['POST', 'GET'])
@user.route('/register', methods=['POST', 'GET'])
def register():
    """注册用户试图
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data, form.email.data)
        user.save(user)
        login_user(user, True, False)
        return redirect(url_for('index'))
    return render_template('/user/register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
@user.route('/login', methods=['POST', 'GET'])
@login_required
def login():
    """登录用户视图
    """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        u = User.has_username(form.username.data)
        if not u:
            flash(u'无此用户', 'warning')
            return render_template('/user/login.html', form=form, title=u'登录')
        if not u.is_correct_password(form.password.data):
            flash(u'密码错误', 'error')
            return render_template('/user/login.html', form=form, title=u'登录')
        u.dologin()
        """如果输入的登录用户名和密码都正确则成功跳转到系统主页
        """
        flash(u' %s 登录成功' % form.username.data)
        return redirect(url_for('index'))

    return render_template('/user/login.html', form=form, title=u'登录')


@app.route('/logout')
@user.route('/logout')
def logout():
    """用户登出方法
    """
    session.pop('username', None)
    session.pop('password', None)
    flash(u"登出成功")
    return redirect(url_for('index'))


@user.route('/info', methods=['POST', 'GET'])
def info():
    """显示用户信息方法
    """
    g.user = User()
    form = SettingForm()
    g.user.is_login()
    form.username = g.user.username
    form.password = g.user.password
    form.email = g.user.email
    return render_template('/user/info.html', form=form, title=u'用户信息')


@user.route('/setting', methods=['POST', 'GET'])
def setting():
    """设置用户信息方法
    """
    g.user = user = User.is_login()
    form = SettingForm()
    u = User()
    if request.method == 'POST':
        if not u.has_username(form.username.data) or session['username'] == form.username.data:
            """如果修改后的用户名不存在数据库或者和当前登录的用户名相同则更新数据库中对应的记录"""
            if form.username.data == "":
                flash(u'用户名不能为空', 'error')
                return render_template('/user/setting.html', form=form, title=u'修改设置')
            if form.password.data == "":
                flash(u'密码不能为空', 'error')
                return render_template('/user/setting.html', form=form, title=u'修改设置')
            if form.email.data == "":
                flash(u'邮箱不能为空', 'error')
                return render_template('/user/setting.html', form=form, title=u'修改设置')
            if not u.edit(user, form.username.data, form.password.data, form.email.data):
                """写入数据库"""
                flash(u'修改失败', 'error')
                return render_template('/user/setting.html', form=form, title=u'修改设置')
            user.dologin()
            flash(u'用户信息修改成功')
            return redirect(url_for('index'))
        else:
            flash(u'用户已存在', 'warning')
            return render_template('/user/setting.html', form=form, title=u'修改设置')
    else:
        form.username = user.username
        form.password = user.password
        form.email = user.email
        return render_template('/user/setting.html', form=form, title=u'修改设置')
    
    
