# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect
from app.models.Fundbook import Fundbook
from app.models.Picture import Picture
from app.models.Subject import Subject
from app.helpers.pagination import get_page_items, get_pagination
from app.forms.fundbook import FundbookForm
from app import db

fundbook = Blueprint('fundbook', __name__, template_folder='fundbook')


@fundbook.route('/', )
@fundbook.route('/index')
def fundbook_index():
    """发票列表

    不再编写模板，请参考 Person 相关的模板
    有必要掌握 Bootstrap3
    """
    rank = request.args.get('rank', 'id')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')

    page, per_page, offset = get_page_items()
    fundbooks = Fundbook.find(search=search, order=order, rank=rank)
    pagination = get_pagination(page=page, total=fundbooks.count())

    return render_template('/fundbook/index.html',
                           fundbooks=fundbooks.offset(offset).limit(per_page),
                           pagination=pagination,
                           search=search, order=order)


@fundbook.route('/<int:id>')
def fundbook_info(id):
    """显示单张发票信息
    """

    inv = Fundbook.query.get(id)
    return render_template('/fundbook/info.html',
                           fundbook=inv)


@fundbook.route('/new', methods=['POST', 'GET'])
def fundbook_new():
    """添加发票

    使用 WTForm 来创建表单并验证和获取表单内容
    """
    form = FundbookForm(request.form)

    if request.method == 'POST' and form.validate():
        inv = Fundbook()
        form.populate_obj(inv)
        db.session.add(inv)
        inv.save()
        print 'ni'
        flash(u'成功添加经费本')
        return redirect('/fundbook/%d' % int(inv.id))
    return render_template('/fundbook/edit.html', form=form, title=u'个人')


@fundbook.route('/<int:id>/edit', methods=['POST', 'GET'])
def fundbook_edit(id):
    """编辑发票

    和添加类似，参加 Person 的实现
    """

    ren = Fundbook.query.get(id)
    """在数据库中查找到这个对象"""
    form = FundbookForm(request.form, obj=ren)
    if request.method == 'POST' and form.validate():
        form.populate_obj(ren)
        """对于编辑操作，则不需要添加，但是需要实现在数据库中查找到对象"""
        ren.save()
        flash(u'成功更新个人信息')
        return redirect('/fundbook/%d' % id)
    return render_template('/fundbook/edit.html', form=form, title=u'编辑个人')
