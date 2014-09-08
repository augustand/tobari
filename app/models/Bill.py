# -*- coding:utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Text, or_, asc, desc

from app import db


class Bill(db.Model):
    """账单

    导入的整张账单，对应多个账目
    """
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True)

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    bank = Column(String)
    """账单所属银行
    """

    html = Column(Text)
    """导入的 HTML 数据
    """
    html_file = ""
    
    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找
        """
        if search:
            return Bill.query.filter(
                    Bill.bank.like("%%%s%%" % search),
                    ).order_by(eval(("%s(Bill.%s)" % (order, rank))))
        else:
            return Bill.query.order_by(eval(("%s(Bill.%s)" % (order, rank))))
        
        
    @staticmethod
    def save():
        """保存，提交到数据库
         """
        db.session.commit()

