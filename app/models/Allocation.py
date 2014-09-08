# -*- coding:utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey

from app import db


class Allocation(db.Model):
    """经费分配表
    """
    __tablename__ = 'allocations'
    
    id = Column(Integer, primary_key=True)
    
    create_time = Column(DateTime, default=datetime.now)
    
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    beneficiary_id = Column(Integer, ForeignKey('people.id'))
    """收益人
    
    即该金额最后补给谁了（可以不是实际的出资人受益）
    """
    
    approve_paper_id = Column(Integer, ForeignKey('approvals.id'))
    """审批单ID"""
    
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    """发票ID，票上有金额"""
    
    used_type = Column(Enum(
        'invoice', 'travelGrants',
        'labor', 'loan', 'repayment',
        'limitReport', 'taxes',
        'invoiceAndBillOfDifference',
        name='USEDTYPE'))
    """类型：
    
    * 发票报账
    * 差旅补助
    * 劳务费
    * 借款 （值正数）
    * 还款 （值负数）
    * 限报（值负数）
    * 税费（值负数）
    * 发票与账单差额
    
    **可以通过此差额找到发票和账单的不同，从而计算最后对账单和实际到帐的差额**
    **还款时报账的信息单独增加多条记录**
    """
    
    payment = Column(Integer)
    """忠实记录每笔发票或补助等收支金额
    """
    
