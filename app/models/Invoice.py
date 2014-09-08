# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Text,or_, asc, desc, and_
from sqlalchemy.orm import relationship, backref
from app.models.Allocation import Allocation
from app import db


class Invoice(db.Model):
    """发票的信息"""

    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    allocations = relationship("Allocation")
    """发票信息ID"""

    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relationship("Subject")
    """科目"""

    picture_id = Column(Integer, ForeignKey('pictures.id'))
    picture = ""
    image = relationship("Picture")
    """照片"""

    amount = Column(Integer)
    """发票金额"""

    account_id = Column(Integer, ForeignKey('accounts.id'))
    accounts = relationship("Account")
    """账单号"""

    invoice_date = Column(DateTime)
    """发票票面日期"""

    description = Column(String)
    """发票汇总内容"""

    detail = Column(String)
    """发票内容明细"""

    is_consumed = Column(Boolean)
    """是否为未消费的票"""

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    
    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找
        
        理论上还可以进一步简化
        """
        
        if search:
            return Invoice.query.filter(
                or_(
                    Invoice.name.like("%%%s%%" % search),
                    Invoice.office.like("%%%s%%" % search),
                    Invoice.job_number.like("%%%s%%" % search),
                    Invoice.telephone.like("%%%s%%" % search),
                    Invoice.identity_card.like("%%%s%%" % search),
                    Invoice.business_card_id.like("%%%s%%" % search),
                    Invoice.debit_card_id.like("%%%s%%" % search),
                    Invoice.opening_bank.like("%%%s%%" % search),
                    Invoice.mobile.like("%%%s%%" % search),
                )).order_by(eval(("%s(Invoice.%s)" % (order, rank))))
        else:
            return Invoice.query.order_by(eval(("%s(Invoice.%s)" % (order, rank))))
        
  
    @staticmethod
    def find_relation(list):
        paper = 0
        if list[0] == 1:
            if list[2] == None:
                return 0, 0, Invoice.query.filter(and_(Invoice.accounts.card_no != None, Invoice.allocations.id == None,
                                      Invoice.accounts.funder_id == list[1])).\
                                      order_by(desc(Invoice.invoice_date))
            invoice_list = Invoice.query.filter(and_(Invoice.accounts.card_no != None, Invoice.allocations.id == None,
                                      Invoice.accounts.funder_id == list[1], Invoice.accounts.status_index == '=')).\
                                      order_by(desc(Invoice.invoice_date))
            max_money = list[2]
            money = 0
            for inv in invoice_list:
                if money >= max_money:
                    break
                money += inv.amount
                paper +=1
                allocation = Allocation(approve_paper_id = list[3], invoice_id = inv.id)
                db.session.add(allocation)
                db.session.commit()
            if money >=max_money:
                return paper, None
            return paper, money, Invoice.query.filter(and_(Invoice.accounts.card_no != None, Invoice.allocations.id == None,
                                      Invoice.accounts.funder_id == list[1], Invoice.accounts.status_index != '=')).\
                                      order_by(desc(Invoice.invoice_date))
        if list[2] == 2:
            if list[2] == None:
                return 0, 0, Invoice.query.filter(and_(Invoice.accounts.card_no == None, Invoice.allocations.id == None,
                                      Invoice.accounts.funder_id == list[1])).\
                                      order_by(desc(Invoice.invoice_date))
            invoice_list = Invoice.query.filter(and_(Invoice.accounts.card_no == None, Invoice.allocations.id == None,
                                      Invoice.accounts.funder_id == list[1], Invoice.accounts.status_index == '=')).\
                                      order_by(desc(Invoice.invoice_date))
            max_money = list[2]
            money = 0
            for inv in invoice_list:
                if money >= max_money:
                    break
                money += inv.amount
                paper +=1
                allocation = Allocation(approve_paper_id = list[3], invoice_id = inv.id)
                db.session.add(allocation)
                db.session.commit()
            if money >=max_money:
                return paper, None
            return paper, money, Invoice.query.filter(and_(Invoice.accounts.card_no == None, Invoice.allocations.id == None,
                                      Invoice.accounts.funder_id == list[1], Invoice.accounts.status_index != '=')).\
                                      order_by(desc(Invoice.invoice_date))

    @staticmethod
    def save():
        """保存，提交到数据库
        
        包括添加和修改之后都要执行
        """
        db.session.commit()

   