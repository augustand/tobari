# -*- coding:utf-8 -*-

from datetime import datetime

from flask import flash
from sqlalchemy import Column, Integer, DateTime, String, Enum, Boolean, ForeignKey, or_, asc, desc, and_
from sqlalchemy.orm import relationship, backref
from app import db
from app.models.Person import Person
from app.models.Invoice import Invoice

class Account(db.Model):
    """账目（账单条目）
    """
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    bill_id = Column(Integer, ForeignKey('bills.id'))
    bill = relationship("Bill", backref = "accounts")
    """导入账单的编号
    """

    funder_id = Column(Integer, ForeignKey('people.id'))
    funder = ""
    funders = relationship("Person", backref = "accounts")
    """出资人"""
    
    transaction_money = Column(Integer)
    """交易金额"""

    currency = Column(String)
    
    def get_forex(self, cur):
        """获得外汇"""
        cur_list = {'USD':10, 'EUR':11, 'GBP':12, 'CNY':1, 'HK':14, 'MOP':15}
        return cur_list[cur]
    
    def get_chinese(self):
        """获得某个币种中文名"""
        cur_list = [('USD', u'美元'), ('EUR', u'欧元'), ('GBP', u'英镑'), ('CNY', u'人民币'), ('HK', u'港币'), ('MOP', u'澳门币')]
        if self.currency == None:
            return None
        return dict(cur_list)[self.currency]
    @staticmethod
    def get_currencies():
        """获得币种和中文名"""
        return [('USD', u'美元'), ('EUR', u'欧元'), ('GBP', u'英镑'), ('CNY', u'人民币'), ('HK', u'港币'), ('MOP', u'澳门币')]
    """币种:
        
        * 美元
        * 欧元
        * 英镑
        * 人民币
        * 港币
        * 澳门币
    """
    
    china_yuan = Column(Integer)
    """实际人民币

    导入时默认使用交易金额，如果不是人民币交易则为空，由用户自己维护正确的金额
    """

    enter_money = Column(Integer)
    """入账金额

    暂时不明白是什么关系，先不对此数字改写
    """

    enter_date = Column(DateTime)
    """记账日

    暂时不明白是什么关系，先不对此数字改写
    """

    card_no = Column(String)
    """卡号后四位

    暂时不改写，使用person_id对应的卡号
    """

    trade_abstract = Column(String)
    """交易摘要
    """

    transaction_place = Column(String)
    """交易地点"""

    is_submit = Column(Boolean)
    """是否需要报销"""

    create_time = Column(DateTime, default=datetime.now)
    """录入日期"""

    status_index = Column(Enum('=', '>', '<', name='STATUS'))
    """发票抵冲账单的记录

    分别用下面的符号表示本账单和发票的关系:
        * =
        * <
        * >
    """
    @staticmethod
    def chage_statusindex(id,invoice):
        """发票抵冲账单的记录值的改变，每当某账目被关联发票，（invoice）invoice_info视图方法调用
        """
        invoices = Invoice.query.filter(Invoice.account_id == id)
        inv_sum = 0
        acc = Account.query.get(id)
        for inv in invoices:
            inv_sum += inv.amount
        if inv_sum+invoice.amount < acc.transaction_money:
            acc.status_index = '<'
        if inv_sum+invoice.amount == acc.transaction_money:
            acc.status_index = '='
        if inv_sum+invoice.amount > acc.transaction_money:
            acc.status_index = '>'
        acc.save()
    
    @staticmethod
    def importbill_save(bills_list, bill_id):
        """HTML账单导入之后经过解析，将所得数据（bills_list）保存到对应的数据库中，此方法被（bill）bill_new视图方法调用
        """
        cur_list = {'USD':10, 'EUR':11, 'GBP':12, 'CNY':1, 'HK':14, 'MOP':15}
        person_id = Person.judge(bills_list[0][2][0][3])
        
        bills_list = bills_list[1][1:-1]
        try:
            for account in bills_list:
                acc = Account()
                acc.funder_id = person_id
                acc.bill_id = bill_id
                acc.is_submit = True
                acc.enter_date = account[0][0]
                acc.card_no = account[2][0]
                acc.trade_abstract = account[3][0]
                acc.transaction_place = account[4][0]
                money_transaction = str(account[5][0]).split('/')
                money_enter = str(account[6][0]).split('/')
                print money_transaction[1]
                acc.transaction_money = float(money_transaction[0])
                acc.currency = money_transaction[1]
                acc.enter_money = float(money_enter[0])
                acc.china_yuan = acc.transaction_money*float(str(cur_list[money_transaction[1]]))
                db.session.add(acc)
                acc.save()
        except:
            return flash(u'保存账单条目失败', 'error')
        return flash(u'保存账单条目成功')
        
    @staticmethod
    def autoadd_bill_save(invoice):
        """在所添加发票没有选择与之关联的帐目的情况下,(invoice）chioce_account视图方法调用此方法
        """
        try:
            account = Account(transaction_money=invoice.amount, enter_date=invoice.invoice_date, currency='CNY', 
                              status_index='=', is_submit=True)
            account.china_yuan=invoice.amount*int(account.get_forex('CNY'))
            db.session.add(account)
            account.save()
        except:
            return 0
        return account.id
    
    @staticmethod
    def find(search=None, rank='id', order='asc'):
        """按条件查找
        
        理论上还可以进一步简化
        """
        
        if search:
            return Account.query.filter(
                or_(
                    Account.bill_id.like("%%%s%%" % search),
                    Account.funder_id.like("%%%s%%" % search),
                    Account.currency.like("%%%s%%" % search),
                )).order_by(eval(("%s(Account.%s)" % (order, rank))))
        else:
            return Account.query.order_by(eval(("%s(Account.%s)" % (order, rank))))
        
        
    @staticmethod
    def search(date, money, rank='id', order='asc'):
        """按条件查找
        
        理论上还可以进一步简化
        """
        import datetime
        min_date = date-datetime.timedelta(days=5)
        return Account.query.filter(
            and_(Account.enter_date <= date, 
                Account.enter_date >= min_date
            )).filter(or_(Account.status_index == '<', Account.status_index == None)).order_by(eval(("%s(Account.%s)" % (order, rank))))
        
    @staticmethod
    def save():
        """保存，提交到数据库
        
        包括添加和修改之后都要执行
        """
        db.session.commit()

   

