# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import validators
from wtforms.fields import FileField
from wtforms.validators import DataRequired, regexp
from app.models.Invoice import Invoice

class ImageForm(Form):
    """照片信息
    
    其他和发票有关的表单都放在这个文件中
    注意，新版本的 WTForm 用 StringField 替代了 TextField，其他变化和 API 请查阅文档
    """
    picture = FileField(u'Image File')

# class UploadForm(Form):
# image = FileField(u'Image File', validators=[validators.regexp(u'^[^/\\]\.jpg$')])
# def validate_image(form, field):
# if field.data:
# field.data = re.sub(r’[^a-z0-9_.-]’, ’_’, field.data)
# def upload(request):
# form = UploadForm(request.POST)
# if form.image.data:
# image_data = request.FILES[form.image.name].read()
# open(os.path.join(UPLOAD_PATH, form.image.data), ’w’).write(image_data)
