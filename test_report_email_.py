# -*- coding:utf-8 -*-
import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time


class Mailer(object):
    def __init__(self, maillist, mailtitle, mailcontent):
        self.mail_list = maillist
        self.mail_title = mailtitle
        self.mail_content = mailcontent
        # self.mail_host = "smtp.QQ.com"  # SMTP服务器
        # self.mail_user = "975405349"  # 用户名
        # self.mail_pass = "xlmbxdfmuryfbdjh"  # 授权密码，非登录密码
        self.mail_host = "smtp.sina.cn"
        self.mail_user = "wangyue_131"
        self.mail_pass = "sxy5201314"
        self.mail_postfix = "sina.cn"
        # self.mail_postfix = "QQ.com"

    def sendMail(self):
        me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        msg = MIMEMultipart()
        msg['Subject'] = '调资文件'
        msg['From'] = me
        msg['To'] = ";".join(self.mail_list)

        # puretext = MIMEText('<h1>你好，<br/>'+self.mail_content+'</h1>','html','utf-8')
        puretext = MIMEText('纯文本内容' + self.mail_content,'base64', 'utf-8')
        msg.attach(puretext)
        report_dir=r"C:\Python27\flask_test\diaozi1\result"
        lists = os.listdir(report_dir)
        lists.sort(key=lambda fn: os.path.getatime(report_dir + '\\' + fn ))
        file = os.path.join(report_dir, lists[-1])
        # jpg类型的附件
        # jpgpart = MIMEApplication(open('/home/mypan/1949777163775279642.jpg', 'rb').read())
        # jpgpart.add_header('Content-Disposition', 'attachment', filename='beauty.jpg')
        # msg.attach(jpgpart)
        file_time = time.strftime('%Y%m%d%S', time.localtime(time.time()))
        #首先是xlsx类型的附件
        xlsxpart = MIMEApplication(open(file, 'rb').read())
        xlsxpart.add_header('Content-Disposition', 'attachment', filename=file_time+'result'+'.'+"xlsx")
        msg.attach(xlsxpart)

        # mp3类型的附件
        # mp3part = MIMEApplication(open('kenny.mp3', 'rb').read())
        # mp3part.add_header('Content-Disposition', 'attachment', filename='benny.mp3')
        # msg.attach(mp3part)

        # pdf类型附件
        # part = MIMEApplication(open('foo.pdf', 'rb').read())
        # part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
        # msg.attach(part)

        try:
            s = smtplib.SMTP_SSL( )  # 创建邮件服务器对象
            s.connect(self.mail_host)  # 连接到指定的smtp服务器。参数分别表示smpt主机和端口
            s.login(self.mail_user, self.mail_pass)  # 登录到你邮箱
            s.sendmail(me, self.mail_list, msg.as_string())  # 发送内容
            s.close()
            return True
        except Exception as e:
            print (str(e))
            return False
if __name__ == '__main__':
    # send list
    mailto_list = ["wangyue@daihoubang.com", "wangyue_131@163.com","975405349@qq.com"]
    mail_title = 'Hey subject'
    mail_content = 'Hey this is content'
    mm = Mailer(mailto_list, mail_title, mail_content)
    res = mm.sendMail()
    print (res)


# import smtplib
# from email.header import Header
# from email.mime.text import MIMEText
#
# # 第三方 SMTP 服务
# mail_host = "smtp.QQ.com"  # SMTP服务器
# mail_user = "975405349"  # 用户名
# mail_pass = "xlmbxdfmuryfbdjh"  # 授权密码，非登录密码
#
# sender = "975405349@qq.com"
# receivers=["18018564752@163.com","wangyue@daihoubang.com"]
#
#
#
# content = '我用Python'
# title = '人生苦短'  # 邮件主题
#
#
# def sendEmail():
#     message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
#     message['From'] = "{}".format(sender)
#     message['To'] = ",".join(receivers)
#     message['Subject'] = title
#
#     try:
#         smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
#         smtpObj.login(mail_user, mail_pass)  # 登录验证
#         smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
#         print("mail has been send successfully.")
#     except smtplib.SMTPException as e:
#         print(e)
#
#
# def send_email2(SMTP_host, from_account, from_passwd, to_account, subject, content):
#     email_client = smtplib.SMTP(SMTP_host)
#     email_client.login(from_account, from_passwd)
#     # create msg
#     msg = MIMEText(content, 'plain', 'utf-8')
#     msg['Subject'] = Header(subject, 'utf-8')  # subject
#     msg['From'] = from_account
#     msg['To'] = to_account
#     email_client.sendmail(from_account, to_account, msg.as_string())
#
#     email_client.quit()
#
#
# if __name__ == '__main__':
#     sendEmail()
    # receiver = '***'
    # send_email2(mail_host, mail_user, mail_pass, receiver, title, content)
