# -*- coding:utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, or_ , asc, desc

from app import db


class Fundbook(db.Model):

    """经费本"""
    __tablename__ = 'fundbooks'
    
    id = Column(Integer, primary_key=True)

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    project_code = Column(String, nullable=False)
    """项目代码"""

    principal = Column(String, nullable=False)
    """负责人"""

    total_amount = Column(Integer)
    """经费总额"""

    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找

        理论上还可以进一步简化
        """

        if search:
            return Fundbook.query.filter(
                or_(
                    Fundbook.project_code.like("%%%s%%" % search),
                    Fundbook.principal.like("%%%s%%" % search),
                    Fundbook.total_amount.like("%%%s%%" % search)
                )).order_by(eval(("%s(Fundbook.%s)" % (order, rank))))
        else:
            return Fundbook.query.order_by(eval(("%s(Fundbook.%s)" % (order, rank))))

    @staticmethod
    def save():
        """保存，提交到数据库

        包括添加和修改之后都要执行
        """
        db.session.commit()
