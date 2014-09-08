# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect
from app.models.Fund import Fund
from app.models.Picture import Picture
from app.models.Subject import Subject
from app.helpers.pagination import get_page_items, get_pagination
from app import db
from app.forms.fund import FundForm


fund = Blueprint('fund', __name__, template_folder='fund')


@fund.route('/', )
@fund.route('/index')
def fund_index():
    """发票列表

    不再编写模板，请参考 Person 相关的模板
    有必要掌握 Bootstrap3
    """
    rank = request.args.get('rank', 'id')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')

    page, per_page, offset = get_page_items()
    funds = Fund.find(search=search, order=order, rank=rank)
    pagination = get_pagination(page=page, total=funds.count())

    return render_template('/fund/index.html',
                           funds=funds.offset(offset).limit(per_page),
                           pagination=pagination,
                           search=search, order=order)


@fund.route('/<int:id>')
def fund_info(id):
    """显示单张发票信息
    """

    inv = Fund.query.get(id)
    return render_template('/fund/info.html',
                           fund=inv)


@fund.route('/new', methods=['POST', 'GET'])
def fund_new():
    """添加发票

    使用 WTForm 来创建表单并验证和获取表单内容
    """
    form = FundForm(request.form)

    if request.method == 'POST' and form.validate():
        inv = Fund()
        form.populate_obj(inv)
        db.session.add(inv)
        inv.save()
        flash(u'成功添加经费本')
        return redirect('/fund/%d' % int(inv.id))
    return render_template('/fund/edit.html', form=form, title=u'编辑个人')

@fund.route('/<int:id>/edit', methods=['POST', 'GET'])
def fund_edit(id):
    """编辑发票

    和添加类似，参加 fund 的实现
    """

    ren = Fund.query.get(id)
    """在数据库中查找到这个对象"""
    form = FundForm(request.form, obj=ren)
    if request.method == 'POST' and form.validate():
        form.populate_obj(ren)
        """对于编辑操作，则不需要添加，但是需要实现在数据库中查找到对象"""
        ren.save()
        flash(u'成功更新个人信息')
        return redirect('/fund/%d' % id)
    return render_template('/fund/edit.html', form=form, title=u'编辑个人')
