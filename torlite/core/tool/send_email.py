# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from config import smtp_cfg


def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me="云算笔记"+"<"+smtp_cfg['user']+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(smtp_cfg['host'])  #连接smtp服务器
        s.login(smtp_cfg['user'],smtp_cfg['pass'])  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except :
        return False
if __name__ == '__main__':
    if send_mail([],"This is subject","<a href='http://www.yunsuan.org'>Yun Suan Site</a>"):
        print ("Success!")
    else:
        print( "False!")