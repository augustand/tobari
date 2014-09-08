# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Enum, ForeignKey, or_ , asc, desc
from sqlalchemy.orm import relationship, backref
from app import db

class Approval(db.Model):
    """审批单表
    """
    __tablename__ = 'approvals'

    id = Column(Integer, primary_key=True)
    """审批单表ID"""
    
    picture_id = Column(Integer, ForeignKey('pictures.id'))
    picture = ""
    image = relationship("Picture")
    """审批单照片"""
    
    agent_id = Column(Integer, ForeignKey('people.id'))
#     aget = relationship("Person", backref=backref('agett', order_by=id))
    """经办人ID"""
    
    fund_id = Column(Integer, ForeignKey('funds.id'))
    fund = relationship("Fund")
    """经费条目ID"""

    invoice_count = Column(Integer)
    """发票张数"""

    payee_id = Column(Integer, ForeignKey('people.id'))
#     payee = relationship("Person", backref=backref('payeee', order_by=id))
    """收款人ID"""

    subject_list = Column(String)
    """科目单"""

    approval_type = Column(String)
    
    @staticmethod
    def get_approval_type():
        return [('OrdinaryReimbursement', u'普通报账'), ('Labor', u'劳务费'), ('Repayment', u'借款单'), ('Borrowing', u'还款单')]
    
    def get_chinese_approval(self):
        approvaltype_list = [('OrdinaryReimbursement', u'普通报账'), ('Labor', u'劳务费'), ('Repayment', u'借款单'), ('Borrowing', u'还款单')]
        return dict(approvaltype_list)[self.approval_type]
    """审批单类型

    * 普通报账
    * 劳务费
    * 借款单
    * 还款单
    """

    status = Column(String)
    
    @staticmethod
    def get_status():
        return [('Printed', u'已打印'), ('Approvaling', u'审批中'), ('Deliveried', u'已投递'), ('CompleteReimbursement', u'完成报账')]
    
    def get_chinese_status(self):
        status_list = [('Printed', u'已打印'), ('Approvaling', u'审批中'), ('Deliveried', u'已投递'), ('CompleteReimbursement', u'完成报账')]
        return dict(status_list)[self.status]
    """上报状态
    
    * 已打印
    * 审批中
    * 已投递
    * 完成报账
    """

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    
    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找
        
        理论上还可以进一步简化
        """
    
        if search:
            return Approval.query.filter(
                or_(
                    Approval.picture_id.like("%%%s%%" % search),
                    Approval.agent_id.like("%%%s%%" % search),
                    Approval.fund_id.like("%%%s%%" % search),
                    Approval.invoice_count.like("%%%s%%" % search),
                    Approval.payee_id.like("%%%s%%" % search),
                )).order_by(eval(("%s(Approval.%s)" % (order, rank))))
        else:
            return Approval.query.order_by(eval(("%s(Approval.%s)" % (order, rank))))
        
    @staticmethod
    def save():
        """保存，提交到数据库
        
        包括添加和修改之后都要执行
        """
        db.session.commit()







