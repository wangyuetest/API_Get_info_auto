#coding:utf-8
import MySQLdb
import xlwt,xlrd
import os
from test_report_email_ import *
import time
db_host="10.76.2.2"
# db_port=3306
db_user="admin_readonly"
db_password="Collect@2017#dhb"
db_data="collect"
# port=db_port,
file_time =time.strftime('%Y%m%d%S',time.localtime(time.time()))
result_dir=r"C:\Python27\flask_test\diaozi1\result"
db=MySQLdb.connect(host=db_host,user=db_user,passwd=db_password,db=db_data)

wb = xlwt.Workbook(encoding='utf-8')  # 创建一个excel工作簿，编码utf-8，表格中支持中文
sheet = wb.add_sheet('sheet 1')  # 创建一个sheet
cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)  # 创建一个指针对象
#查询SQL
cursor.execute("SELECT called_no,feedback FROM soft_phone_clear_details_info WHERe 	create_date > '2018-08-07 00:00:00'AND create_date < '2018-08-07 23:59:59'AND batch_id = '55166e318c8e498bb242b2fa4f8f9cba'AND feedback != ''")  # 执行sql语句
results = cursor.fetchall()
print results
#获取查询结果
columnName = []
col=results[0].keys()

for i in col:
    columnName.append(i)

# columnName.append("statusnames")
columnLen = len(columnName)

for i in range(columnLen):  # 将列名插入表格
    sheet.write(0, i, columnName[i])


rows = len(results)  # 获取行数

dict = {
    "dealing": "已接",
    "notDeal": "未接",
    "leak": "放弃(未接)",
    "blackList": "黑名单",
    "voicemail": "留言",
    "user_busy": "用户正忙",
    "call_reminder": "来电提醒",
    "unavailable": "无法接通",
    "call_barring": "呼叫限制",
    "call_divert": "呼叫转移",
    "shutdown": "关机",
    "halt": "停机",
    "vacant_number": "空号",
    "in_the_call": "正在通话中",
    "network_is_busy": "网络忙",
    "overtime": "超时",
    "short_tone": "短忙音",
    "long_tone": "长忙音",
    "unanswered_ringing": "振铃未接",
    "phone_null": "号码为空",
    "unknown": "未知",
    "local_arrearage":"本机已欠费"


 }
for i in range(0,rows):
    for j in range(columnLen):
        if(j==0):
         sheet.write(i + 1, j, results[i][columnName[j]])
        else:
           sheet.write(i + 1, j,dict[results[i][columnName[j]]])


if __name__=='__main__':
    wb.save(result_dir+"/"+file_time+'clear'+'.'+"xlsx")
    mailto_list = ["wangyue@daihoubang.com"]
    mail_title = 'Hey subject'
    mail_content = 'Hey this is content'
    mm = Mailer(mailto_list, mail_title, mail_content)
    res = mm.sendMail()
    print res
    # 保存表格
    print '保存表格成功'
    cursor.close()
    db.close()