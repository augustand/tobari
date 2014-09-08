# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect

from app.models.Person import Person
from app.forms.person import PersonForm

from app import app, db
from app.helpers.pagination import get_page_items, get_pagination

person = Blueprint('person', __name__, template_folder='person')

@person.route('/', )
@person.route('/index')
def person_index():
    """个人列表
    """
    rank = request.args.get('rank', 'id')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')
    
    page, per_page, offset = get_page_items()
  
    people = Person.find(search=search, order=order, rank=rank)
     
    pagination = get_pagination(page=page, total=people.count())
    
    return render_template('/person/index.html', 
                           people=people.offset(offset).limit(per_page), 
                           pagination=pagination ,
                           search=search,order=order)

@person.route('/<int:id>')
def person_info(id):
    """显示个人信息
    """
    ren = Person.query.get(id)
    return render_template('/person/info.html', person=ren)

@person.route('/new', methods=['POST', 'GET'])
def person_new():
    """添加个人
    """
    form = PersonForm(request.form)
    if request.method == 'POST' and form.validate():
        ren = Person()
        """新建一个对象"""
        form.populate_obj(ren)
        """用 WTForm 自带的方法把表单数据转换成对象里面的属性"""
        db.session.add(ren)
        """对于新建操作，需要调用 add() 来添加这个对象"""
        ren.save()
        """用对象本身实现的 save() 方法来实际写入数据库"""
        flash(u'成功添加个人 %s' % ren.name)
        return redirect('/person/%d' % int(ren.id))
    return render_template('/person/edit.html', form=form, title=u'添加个人')

@person.route('/<int:id>/edit', methods=['POST', 'GET'])
def person_edit(id):
    """编辑个人
    """
    ren = Person.query.get(id)
    """在数据库中查找到这个对象"""
    form = PersonForm(request.form, obj=ren)
    if request.method == 'POST' and form.validate():
        form.populate_obj(ren)
        """对于编辑操作，则不需要添加，但是需要实现在数据库中查找到对象"""
        ren.save()
        flash(u'成功更新个人信息')
        return redirect('/person/%d' % id)
    return render_template('/person/edit.html', form=form, title=u'编辑个人')
