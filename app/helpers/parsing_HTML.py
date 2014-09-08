# -*- coding: UTF-8 -*-
import HTMLParser

class MyParser(HTMLParser.HTMLParser):
    """解析HTML（适用于中国农业银行现阶段的账单文件）"""
    table = 0 #</table> 3->0
    tr = 0 #</tr> 2->0 
    td_flag = 0 #1->0
    td = 0 #</td> 1->0
    
    table_datalist = []#接收账单条目数据
    table_userlist = []#接受账单所属人数据
    tr_datalist = []
    td_datalist = []
    
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)       
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.table +=1
        if tag == 'tr':
            self.tr = 2
        if tag == 'td':
            self.td = 1
       
    def handle_data(self, data):
        if self.table == 4 and self.tr == 2 and self.td == 1:
            self.td_flag = 1
            self.td_datalist.append(data)
            
        if self.table == 1 and self.tr == 2 and self.td == 1:
            self.td_flag = 1
            self.td_datalist.append(data) 
    def handle_endtag(self, tag):
        if tag == 'td' and self.table == 4:
            self.td = 0
            self.tr_datalist.append(self.td_datalist)
            self.td_datalist = []
        if tag == 'tr' and self.td_flag == 1 and self.table == 4:
            self.tr =0
            self.td_flag = 0
            self.table_datalist.append(self.tr_datalist)
            self.tr_datalist = []
            
        if tag == 'td' and self.table == 1:
            self.td = 0
            self.tr_datalist.append(self.td_datalist)
            self.td_datalist = []
        if tag == 'tr' and self.td_flag == 1 and self.table == 1:
            self.tr =0
            self.td_flag = 0
            self.table_userlist.append(self.tr_datalist)
            self.tr_datalist = []
        
               
    def get_tabledata(self):
        return [self.table_userlist, self.table_datalist]
         
        
    
