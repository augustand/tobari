# -*- coding:utf-8 -*-

from datetime import datetime
import tempfile
import os
import time
from sqlalchemy import Column, Integer, DateTime, LargeBinary

from app import db

class Picture(db.Model):
    """照片表
    """
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)

    create_time = Column(DateTime, default=datetime.now)

    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    picture = Column(LargeBinary)
    """照片

    （可以是发票照片、审批单照片）
    """

    def __init__(self, file):
        self.restore(file)

    def restore(self, file):
        filename = tempfile.mktemp()
        file.save(filename)
        output = tempfile.mktemp('.png')
        print 'chulaile'
        os.system('convert %s %s' % (filename, output))
        print 'youmuyou'
        self.picture = open(output).read()

    def url(self):
        dir = '/static/image/restore/'
        filename = '%d_%s.png' % (self.id, self.update_time.strftime('%Y%m%d%H%M%S'))
        filepath = './app%s%s' % (dir, filename)
        if not os.path.isfile(filepath):
            open(filepath, 'w').write(self.picture)
        return '%s%s' % (dir, filename)
        
    @staticmethod
    def save():
        """保存，提交到数据库
        
        包括添加和修改之后都要执行
        """
        db.session.commit()
