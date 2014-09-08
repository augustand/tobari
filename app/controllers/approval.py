# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect
from app.models.Approval import Approval
from app.models.Picture import Picture
from app.models.Person import Person
from app.models.Subject import Subject
from app.models.Invoice import Invoice
from app.helpers.pagination import get_page_items, get_pagination
from app.forms.approval import ApprovalForm
from app import db

approval = Blueprint('approval', __name__, template_folder='approval')




@approval.route('/', )
@approval.route('/index')
def approval_index():
    """审批单列表
    
    不再编写模板，请参考 Person 相关的模板
    有必要掌握 Bootstrap3
    """
    
    rank = request.args.get('rank', 'id')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')
    
    page, per_page, offset = get_page_items()
    approvals = Approval.find(search=search, order=order, rank=rank)
    pagination = get_pagination(page=page, total=approvals.count())

    return render_template('/approval/index.html',
                           approvals=approvals.offset(offset).limit(per_page),
                           pagination=pagination,
                           search=search, order=order)

@approval.route('/<int:id>')
def approval_info(id):
    """显示单个审批单信息
    """
    approval = Approval.query.get(id)
    aget = Person.query.get(approval.agent_id)
    payee = Person.query.get(approval.payee_id)
    info_list = [aget.name, payee.name]
    return render_template('/approval/info.html', approval = approval,info_list = info_list)
    
@approval.route('/new', methods=['POST', 'GET'])
def approval_new():
    """添加审批单
    
    使用 WTForm 来创建表单并验证和获取表单内容
    """
    print('nimei')
    form = ApprovalForm()
    list_subject = [(1, u'公务卡消费'), (2, u'非公务卡消费')]
    form.cost_type.choices = list_subject
    form.subject.choices = Subject.get_subjects()
    print 'nimeimei'
    if request.method == 'POST' and form.validate():
        approval = Approval()
        approval.agent_id = Person.judge(form.agent.data)
        approval.payee_id = Person.judge(form.payee.data)
        approval.subject_list = dict(Subject.get_subjects())[form.subject]
        db.session.add(approval)
        approval.save()
        
        form_list = [form.cost_type, approval.agent_id, form.max_money, approval.id, form.subject]
        invoices = Invoice.find_relation(form_list)
        if invoices[1] == None:
            approval_index = Approval.query.get(approval.id)
            approval_index.invoice_count = invoices[0]
            approval_index.subject_list += (' '+dict(Subject.get_subjects())[form.subject])
            approval_index.status = 'Printed'
            approval.save()
            flash(u'组合成功')
            return redirect('/approval/%d' % int(approval.id))
        return redirect('/approval/%d/chioce' % int(approval.id), incoices) 
    
        
#     if request.method == 'POST' and form.validate():
#         approval = Approval()
#         approval.agent_id = Person.judge(form.agent.data)
#         approval.payee_id = Person.judge(form.payee.data)
#         form.populate_obj(approval)
#         if request.files[form.picture.name]:
#             try:
#                 pic = Picture(request.files[form.picture.name])
#                 db.session.add(pic)
#                 pic.save()
#                 approval.picture_id = pic.id
#             except:
#                 flash(u'图片保存失败', 'error')
#         db.session.add(approval)
#         approval.save()
#         print 'nimei',approval.id
#         flash(u'成功添加审批单')
#         return redirect('/approval/%d' % int(approval.id))
    return render_template('/approval/edit.html', form = form, title=u'添加审批单')

@approval.route('/<int:id>chioce', methods=['POST', 'GET'])
def approval_chioce(id, invoices):
    """选择发票到审批单
    """
    invoices_list = request.args.get('radiobutton')
    page, per_page, offset = get_page_items()
    pagination = get_pagination(page=page, total=invoices[2].count())
    if request.method == 'POST' and form.validate():
        for i in invoices_list:
            allocation = Allocation(approve_paper_id = id, invoice_id = i)
            db.session.add(allocation)
            db.session.commit()
        approval = Approval.query.get(id)
        approval.invoice_count = invoices[1]+invoices_list.length
        approval.save()
        return redirect('/approval/%d' % id)
    
    return render_template('/approval/chioce.html',
                           approvals=invoices[2].offset(offset).limit(per_page),
                           pagination=pagination, content_list = [invoices[0],invoices[1]]
                           )
    
@approval.route('/<int:id>/edit', methods=['POST', 'GET'])
def approval_edit(id):
    """编辑发票
    
    和添加类似，参加 Person 的实现
    """
    approval = Approval.query.get(id)
    form = ApprovalForm(request.form, obj=approval)
    form.status.choices = Approval.get_status()
    form.approval_type.choices = Approval.get_approval_type()
    if request.method == 'POST' and form.validate():
        form.populate_obj(approval)
        
        if request.files[form.picture.name]:
            try:
                pic = Picture.query.get(approval.picture_id)
                if pic:
                    pic.restore(request.files[form.picture.name])
                    pic.save()
                else:
                    pic = Picture(request.files[form.picture.name])
                    db.session.add(pic)
                    pic.save()
                    approval.picture_id = pic.id
            except:
                flash(u'图片保存失败', 'error')
        approval.save()
        flash(u'成功更新审批单信息')
        return redirect('/approval/%d' % id)
    
    return render_template('/approval/edit.html', form = form, title=u'编辑审批单')



