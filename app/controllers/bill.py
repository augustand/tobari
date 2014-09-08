# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect
from app.models.Bill import Bill
from app.models.Account import Account
from app.helpers.pagination import get_page_items, get_pagination
from app.helpers.parsing_HTML import MyParser
from app.forms.bill import BillForm
from app import db
import tempfile
import sys
import sys
reload(sys)
sys.setdefaultencoding('utf8')

bill = Blueprint('bill', __name__, template_folder='bill')

@bill.route('/', )
@bill.route('/index', methods=['POST', 'GET'])
def bill_index():
    """账单列表
    """
    rank = request.args.get('rank', 'id')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')

    page, per_page, offset = get_page_items()
    bills = Bill.find(search=search, order=order, rank=rank)
    pagination = get_pagination(page=page, total=bills.count())
    return render_template('/bill/index.html',
                           bills=bills.offset(offset).limit(per_page),
                           pagination=pagination,
                           search=search, order=order)


@bill.route('/<int:id>')
def bill_info(id):
    """显示账单
    """
    return render_template('/bill/info.html')    

    

@bill.route('/import', methods=['POST', 'GET'])
@bill.route('/new', methods=['POST', 'GET'])
def bill_new():
    """添加账单
    
    POST 步骤：
        1. 获取上传的文件
        2. 解析 HTML
        3. 将解析出来的数据写入数据库
        4. 跳转到 /<int:id>
    """
    form = BillForm(request.form)
    if request.method == 'POST' and form.validate():
        bill = Bill()
        print request.files[form.html_file.name]
        form.populate_obj(bill)
        if request.files[form.html_file.name]:
            try:
                file = request.files[form.html_file.name]
                filename = tempfile.mktemp()
                file.save(filename)
                parser = MyParser()
                parser.feed(open(filename).read())
                bill.html = str(parser.get_tabledata())
                db.session.add(bill)
                db.session.commit()
                Account.importbill_save(parser.get_tabledata(), bill.id)
            except:
                flash(u'文件保存失败', 'error')
        flash(u'成功导入账单')
#         return redirect('/bill/%d' % int(bill.id))

    return render_template('/bill/edit.html', form = form, title=u'添加账单')

@bill.route('/<int:id>/edit', methods=['POST', 'GET'])
def bill_edit(id):
    """编辑账单
    """
    
    return render_template('/bill/edit.html', title=u'编辑账单')
