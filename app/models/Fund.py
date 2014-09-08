# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, or_ , asc, desc
from sqlalchemy.orm import relationship, backref
from app.models.Fundbook import Fundbook
from app import db


class Fund(db.Model):

    """财务处记录 需要从每个经费拥有人的财务记录导入!"""

    __tablename__ = 'funds'

    id = Column(Integer, primary_key=True)
    """经费条目表ID""" 

    fundbook_id = Column(Integer, ForeignKey('fundbooks.id'))
    fundbooks = relationship('Fundbook')
    """经费本ID"""

    income = Column(Integer)
    """收入"""

    expend = Column(Integer)
    """支出"""

    abtract = Column(Text)
    """摘要"""

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找

        理论上还可以进一步简化
        """

        if search:
            return Fund.query.filter(
                or_(
                    Fund.fundbook_id.like("%%%s%%" % search),
                    Fund.income.like("%%%s%%" % search),
                    Fund.expend.like("%%%s%%" % search)
                )).order_by(eval(("%s(Fund.%s)" % (order, rank))))
        else:
            return Fund.query.order_by(eval(("%s(Fund.%s)" % (order, rank))))

    @staticmethod
    def save():
        """保存，提交到数据库

        包括添加和修改之后都要执行
        """
        db.session.commit()
