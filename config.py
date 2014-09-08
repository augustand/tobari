# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "postgresql://tobari:tobari@localhost/tobari"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db')

# WHOOSH_BASE = "postgresql+psycopg2://weibo:weibo@localhost/weiboindex"
# MAX_SEARCH_RESULTS = 50

CSRF_ENABLED = True
SECRET_KEY = 'HappinessChargePrecure'

# 管理员列表
ADMINS = ['anytjf@live.com']

# 语言
LANGUAGES = {
    'cn': '中文（简体）',
    'ja': '日本語',
    'en': 'English'
}

PER_PAGE = 10
LINK_SIZE = ''
CSS_FRAMEWORK = 'bootstrap3'
