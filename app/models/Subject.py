# coding=utf-8
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Text, String, or_, asc, desc
from sqlalchemy.orm import relationship, backref
from app import db


class Subject(db.Model):
    """科目表"""

    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    """科目表ID"""

    name = Column(String(10), unique=True)
    """ 费用类型

    * 交通费  Transportation
    * 住宿费  Accommodation
    * 材料费  Material
    * 查新费  Novelty
    * 五金费  Hardware
    * 会议费  Conference
    * 试剂材料费  ReagentMaterial
    * 设备  Device
    * 工程与维修费  EngineeringAndMaintenance
    * 劳务费  Labor
    * 招待费  Hospitality
    * 版面费  Layout
    * 印刷费  Printing
    * 图书费  Books
    """

    description = Column(Text)
    """科目介绍"""

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找
        
        理论上还可以进一步简化
        """
        
        if search:
            return Subject.query.filter( Subject.name.like("%%%s%%" % search)
                ).order_by(eval(("%s(Subject.%s)" % (order, rank))))
        else:
            return Subject.query.order_by(eval(("%s(Subject.%s)" % (order, rank))))
        
    @staticmethod
    def save():
        """保存，提交到数据库
        
        包括添加和修改之后都要执行
        """
        db.session.commit()
    
    
    @staticmethod
    def get_subjects():
        return [(g.id, g.name) for g in Subject.query.order_by('name')]
