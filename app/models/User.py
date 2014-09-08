# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5
import urllib
import hashlib

from flask import session, g
from sqlalchemy import Column, Integer, DateTime, String

from app import db
from config import SECRET_KEY


class User(db.Model):
    """登录用户表
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    username = Column(String(32), nullable=False, unique=True)
    """用户名"""

    email = Column(String(32))
    """电子邮箱"""

    password = Column(String(64), nullable=False)
    """密码"""

    @staticmethod
    def has_username(username):
        """判断用户是否存在，若存在返回True，否则返回False
        """
        user = User.query.filter_by(username=username).first()
        g.user = user
        if user:
            return user
        else:
            return False

    def is_correct_password(self, password):
        """判断用户的密码正确与否，正确则返回True，否则返回False"""
        m = md5()
        m.update(password)
        m.update(SECRET_KEY)
        if self.password == m.hexdigest():
            return True
        else:
            return False

    def dologin(self):
        """记录当前登录用户信息到session
        """
        session['username'] = self.username
        session['password'] = self.password
        g.user = self

    def init_user(self, username, password, email):
        self.username = username
        self.email = email
        self.password = User.crtpy_password(password)
        return self

    def is_active(self):
        return True

    @staticmethod
    def crtpy_password(password):
        m = md5()
        m.update(password)
        m.update(SECRET_KEY)
        m.hexdigest()
        return m.hexdigest()

    @staticmethod
    def is_login():
        if 'username' in session:
            user = User.has_username(session['username'])
            if not user:
                return False
            if user.password != session['password']:
                return False
            user.dologin()
            g.user = user
            return user
        else:
            return False

    def save(self, user=None):
        if user:
            db.session.add(user)
        db.session.commit()

    @staticmethod
    def get(user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    def edit(self, user, username, password, email):
        """修改用户信息
        """
        try:
            m = md5()
            m.update(str(password))
            m.update(SECRET_KEY)
            user.username = username
            user.password = m.hexdigest()
            user.email = email
            db.session.commit()
        except:
            return False
        else:
            return True

    def avatar(self, size=20, default='mm'):
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(str(self.email).lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
        return gravatar_url
    
    
            
            