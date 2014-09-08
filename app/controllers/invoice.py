# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, flash, redirect
import datetime
from app.models.Invoice import Invoice
from app.models.Picture import Picture
from app.models.Subject import Subject
from app.models.Account import Account
from app.helpers.pagination import get_page_items, get_pagination
from app.forms.invoice import InvoiceForm
from app import db


invoice = Blueprint('invoice', __name__, template_folder='invoice')


@invoice.route('/', )
@invoice.route('/index')
def invoice_index():
    """发票列表
    
    不再编写模板，请参考 Person 相关的模板
    有必要掌握 Bootstrap3
    """
    """个人列表
    """

    rank = request.args.get('rank', 'id')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')

    page, per_page, offset = get_page_items()
    invoices = Invoice.find(search=search, order=order, rank=rank)
    for inv in invoices:
        print inv.invoice_date
    pagination = get_pagination(page=page, total=invoices.count())
    return render_template('/invoice/index.html',
                           invoices=invoices.offset(offset).limit(per_page),
                           pagination=pagination,
                           search=search, order=order)

@invoice.route('/<int:id>/<int:chioce>')
def invoice_info(id, chioce):
    """显示单张发票信息
    """
    if chioce >0: #如果chioce>0则说明用户选中了一帐目和发票关联，需要通过下面的语段进行关联的相关操作后显示发票信息
        invoice = Invoice.query.get(id)
        invoice.account_id = chioce
        Account.chage_statusindex(chioce, invoice)
        invoice.save()
        flash(u'匹配成功')
        flash(u'成功添加发票')
        return render_template('/invoice/info.html',
                           invoice=invoice)
    else:
        invoice = Invoice.query.get(id)
        return render_template('/invoice/info.html',
                           invoice=invoice)
    flash(u'匹配失败', 'error')
    return redirect('/invoice/')

@invoice.route('/new', methods=['POST', 'GET'])
def invoice_new():
    """添加发票
     
        添加发票时会让用户选择关联帐目，若未选择则自动添加一条帐目
    """
    form = InvoiceForm(request.form)
    form.subject_id.choices = Subject.get_subjects()
    if request.method == 'POST' and form.validate():
        inv = Invoice()
        form.populate_obj(inv)
        if request.files[form.picture.name]:
            try:
                pic = Picture(request.files[form.picture.name])
                db.session.add(pic)
                pic.save()
                inv.picture_id = pic.id
            except:
                flash(u'图片保存失败', 'error')
        db.session.add(inv)
        inv.save()
        return redirect('/invoice/%d/chioce' % int(inv.id))
    return render_template('/invoice/edit.html', form=form, title=u'添加发票')
    

@invoice.route('/<int:id>/edit', methods=['POST', 'GET'])
def invoice_edit(id):
    """编辑发票
    
    和添加类似，参加 Person 的实现
    """
    inv = Invoice.query.get(id)
    form = InvoiceForm(request.form, obj=inv)
    form.subject_id.choices = Subject.get_subjects()
    if request.method == 'POST' and form.validate():
        form.populate_obj(inv)
        if request.files[form.picture.name]:
            try:
                pic = Picture.query.get(inv.picture_id)
                if pic:
                    pic.restore(request.files[form.picture.name])
                    pic.save()
                else:
                    pic = Picture(request.files[form.picture.name])
                    db.session.add(pic)
                    pic.save()
                    inv.picture_id = pic.id
            except:
                flash(u'图片保存失败', 'error')
        inv.save()
        flash(u'成功更新个人信息')
        return redirect('/invoice/%d/%d' % (id, id))
    return render_template('/invoice/edit.html', form=form, title=u'编辑发票')
    

@invoice.route('/<int:id>/chioce', methods=['POST', 'GET'])
def chioce_account(id):
    """显示与添加的发票可能会发生关联的帐目
    """
    
    rank = request.args.get('rank', 'enter_date')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')
    invoice = Invoice.query.get(id)
    page, per_page, offset = get_page_items()
    accounts = Account.search(date=invoice.invoice_date, money=invoice.amount, order=order, rank=rank)
    pagination = get_pagination(page=page, total=accounts.count())
    if request.method == 'POST':
        acc_id = Account.autoadd_bill_save(invoice)
        if acc_id !=0:
            return redirect('/invoice/%d/%d' % (id, acc_id))
        flash(u'匹配失败', 'error')
        return redirect('/invoice/')
    return render_template('/invoice/chioce.html',
                           accounts=accounts.offset(offset).limit(per_page),
                           pagination=pagination,
                           search=search, order=order, id=id, chioce=0, title=u'选择关联账目')



