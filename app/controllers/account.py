# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, flash, redirect

from app.models.Account import Account
from app.models.Person import Person
from app.helpers.pagination import get_page_items, get_pagination
from app.forms.account import AccountForm
from app import db

account = Blueprint('account', __name__, template_folder='account')

@account.route('/', )
@account.route('/index')
def account_index():
    """账单条目列表
    
    不再编写模板，请参考 Person 相关的模板
    有必要掌握 Bootstrap3
    """
    """个人列表
    """

    rank = request.args.get('rank', 'id')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')

    page, per_page, offset = get_page_items()
    accounts = Account.find(search=search, order=order, rank=rank)
    pagination = get_pagination(page=page, total=accounts.count())

    return render_template('/account/index.html',
                           accounts=accounts.offset(offset).limit(per_page),
                           pagination=pagination,
                           search=search, order=order)


@account.route('/<int:id>')
def account_info(id):
    """显示单条账单条目信息
    """
    account = Account.query.get(id)
    
    return render_template('/account/info.html',
                           account=account)

@account.route('/new', methods=['POST', 'GET'])
def account_new():
    """添加账单条目
    """
    form = AccountForm(request.form)
    if request.method == 'POST' and form.validate():
        account = Account()
        form.populate_obj(account)
        account.funder_id = Person.judge(form.funder.data)
        account.china_yuan = form.transaction_money.data*account.get_forex(form.currency.data)
        db.session.add(account)
        account.save()
        print 'ni'
        flash(u'成功添加账单条目')
        return redirect('/account/%d' % int(account.id))

    return render_template('/account/edit.html', form=form, title=u'添加账单条目')


@account.route('/<int:id>/edit', methods=['POST', 'GET'])
def account_edit(id):
    """编辑账单条目
    
    和添加类似，参加 Person 的实现
    """
    account = Account.query.get(id)
    form = AccountForm(request.form, obj=account)
    if account.funder_id:
        form.funder.data = account.funders.name
    
    if request.method == 'POST' and form.validate():
        form.populate_obj(account)
        account.funder_id = Person.judge(form.funder.data)
        account.china_yuan = form.enter_money.data*account.get_forex(form.currency.data)
        account.save()
        flash(u'成功更新账单条目信息')
        return redirect('/account/%d' % id)
    return render_template('/account/edit.html', form=form, title=u'编辑账单条目')




