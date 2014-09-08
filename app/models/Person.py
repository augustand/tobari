# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Enum, or_, asc, desc
from sqlalchemy.orm import relationship, backref
from app import db


class Person(db.Model):
    """个人信息表
    
    存储用户卡信息和个人信息
    不用于系统登录
    """
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    telephone = Column(String(15))
    """用户电话"""

    office = Column(String(15))
    """办公室"""

    name = Column(String(16), nullable=False)
    """用户姓名"""

    identity_card = Column(String(18))
    """身份证号"""

    job_number = Column(String(10))
    """工号"""

    business_card_id = Column(String(18))
    """公务信用卡ID"""

    debit_card_id = Column(String(18))
    """借记卡ID"""

    tax_type = Column(Enum('Teacher', 'Student', 'Professor', name='TAXTYPE'))
    def get_chinese(self):
        tax_list = [('Teacher', u'老师'),('Student', u'学生'),('Professor', u'校外专家')]
        return dict(tax_list)[self.tax_type]
    """税类型

    * 校内老师税
    * 学生税
    * 校外专家税
    """
    
    @staticmethod
    def get_tax_type():
        return [('Teacher', u'老师'),('Student', u'学生'),('Professor', u'校外专家')]
    
    opening_bank = Column(String)
    """开户行"""

    mobile = Column(String(20))
    """手机号码"""
    
    @staticmethod   
    def judge(name):
        per = Person.query.filter(Person.name == name).first()
        print per
        if per:
            return per.id
        
        pers = Person(name = name, tax_type = 'Teacher')
        db.session.add(pers)
        db.session.commit()
        return pers.id

    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找
        
        理论上还可以进一步简化
        """
        
        if search:
            return Person.query.filter(
                or_(
                    Person.name.like("%%%s%%" % search),
                    Person.office.like("%%%s%%" % search),
                    Person.job_number.like("%%%s%%" % search),
                    Person.telephone.like("%%%s%%" % search),
                    Person.identity_card.like("%%%s%%" % search),
                    Person.business_card_id.like("%%%s%%" % search),
                    Person.debit_card_id.like("%%%s%%" % search),
                    Person.opening_bank.like("%%%s%%" % search),
                    Person.mobile.like("%%%s%%" % search),
                )).order_by(eval(("%s(Person.%s)" % (order, rank))))
        else:
            return Person.query.order_by(eval(("%s(Person.%s)" % (order, rank))))
        
    @staticmethod
    def save():
        """保存，提交到数据库
        
        包括添加和修改之后都要执行
        """
        db.session.commit()

   