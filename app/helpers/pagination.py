# -*- coding: UTF-8 -*-
from flask import request
from flask_paginate import Pagination


from app import app


def get_page_items():
    page = int(request.args.get('page', 1))
   
    per_page = request.args.get('per_page')
   
    
    if not per_page:
        per_page = app.config.get('PER_PAGE', 10)
    else:
        per_page = int(per_page)
        
    offset = (page - 1) * per_page
    return page, per_page, offset

def get_css_framework():
    return app.config.get('CSS_FRAMEWORK', 'bootstrap3')

def get_link_size():
    return app.config.get('LINK_SIZE', 'sm')

def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      **kwargs
                      )
