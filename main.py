#coding:utf-8
import time
import pandas as pd
import requests
import json
import re
import config
import os
import shutil
import MySQLdb
import xlwt, xlrd
import os
from test_report_email_ import *
import time
from datetime import timedelta
from test_report_email_ import *
from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request,session,redirect,url_for,flash
from werkzeug.security import generate_password_hash
from form import RegisterForm#引入forms.py文件
from login_form import LoginForm
from models import User
from exts import db
import logging
from functools import wraps
# LOG_FORMAT="%(asctime)s=====+++++%(levelname)s++*****++%(message)s"
# logging.basicConfig(filename="tsetdiaozi.log",level=logging.WARNING,format=LOG_FORMAT)
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
with app.app_context():
    db.create_all()
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']=os.urandom(8)
#指定过期时间为7天
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7)
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','csv','gif','GIF'])
# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
# 用于测试上传，稍后用到
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('name'):
            return func(*args,**kwargs)
        else:
           return redirect(url_for('login'))
    return wrapper
@app.route('/',methods=['GET'],strict_slashes=False)
def indexpage():
    return render_template('upload.html')
# 上传文件
@app.route('/',methods=['POST'])
@login_required
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        if fname=='xlsx'or fname=='xls'or fname=='csv' :#判断异常文件并处理
            fname1='upload'+'.'+fname
            unix_time = int(time.time())
            new_filename = str(unix_time)+fname1
        else:
            unix_time = int(time.time())
            new_filename = str(unix_time) + fname  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  #保存文件到upload目录
        return render_template('result.html', var1=fname)
    else:
        return jsonify({"descraption":u"upload a wrong file ","errno": 1001, "errmsg": u"failed",})
        logging.error("a error file!")

@app.route("/login", methods=['GET','POST'])
def login():
    forms =LoginForm()#实例化forms
    if request.method=='POST'and forms.validate_on_submit(): #提交的时候进行验证,如果数据能被所有验证函数接受，则返回true，否则返回false
        data = forms.data#获取form数据信息（包含输入的用户名（account）和密码（pwd）等信息）,这里的account和pwd是在forms.py里定义的
        admin = User.query.filter_by(name=data["account"]).first()#查询表信息admin表里的用户名信息
        if admin == None:
            return  u"账号不存在,请返回重新输入！"#操作提示信息，会在前端显示
        elif admin != None and not admin.check_pwd(data["pwd"]):            #这里的check_pwd函数在models 下Admin模型下定义
            return u"密码错误，请返回重新输入！"
        session['name']= data['account']#匹配成功，添加session
        try:
          return redirect(request.args.get('next') or url_for('indexpage'))#重定向到下一页
        except Exception as e:
          print(e)
    return render_template('login.html',form=forms)
@app.route("/regist", methods=['GET','POST'])
def register():
    form = RegisterForm()#实例化form
    if request.method=='POST'and form.validate_on_submit():#提交时
        data = form.data
        user = User(
            name=data['account'],
            email=data['email'],
            phone = data['phone'],
            pwd=generate_password_hash(data['pwd']),
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功",'ok')
        return redirect(request.args.get('next') or url_for('login'))  # 重定向到首页
    return render_template("regist.html",form=form)
@app.context_processor
def mycontext():
    if session.get('name'):
        return dict(name=session.get('name'))
    else:
        return {}

file_time =time.strftime('%Y%m%d%S',time.localtime(time.time()))
result_dir=r"C:\Python27\flask_test\diaozi1\result"
@app.route("/send_code_A", methods=['POST'])
def send_codeA():
    upload_dir = r'C:\Python27\flask_test\diaozi1\upload'
    report_dir = r"C:\Python27\flask_test\diaozi1\result"
    lists = os.listdir(upload_dir)
    ##申明匿名函数 获取最新访问的文件
    lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
    print(lists[-1])
    # 获取最新的文件
    file = os.path.join(upload_dir, lists[-1])
    if (os.path.exists(report_dir))==False:
        os.mkdir(report_dir)


    def read_excel(file_path):
        user_list = []
        file_df = pd.read_excel(file_path, names=['name', 'idcard', 'phone'])
        for idx, each_row in file_df.iterrows():
            _name = each_row["name"]
            _idcard = each_row["idcard"]
            _phone = each_row["phone"]
            url = 'http://10.76.11.20:82/api/services/cornucopia/rpt_ctc?name=%s&idcard=%s&phone=%s&auth_org=hulushuju' % (
                _name, _idcard, _phone)
            res = requests.get(url)
            data = json.loads(res.text)
            result = data.get("result", [])
            print idx
            if result:
                ctc_lts = result[0].get("contact_list", [])
                if ctc_lts:
                    for i in range(len(ctc_lts)):
                        ctc_lts[i]["uname"] = _name
                        ctc_lts[i]["idcard"] = _idcard
                        ctc_lts[i]["phoneNum"] = _phone
                    user_list.extend(ctc_lts)
        opt_df = pd.DataFrame(user_list)
        opt_df.to_excel(result_dir+"/"+file_time+'A'+'.'+"xlsx", encoding="utf-8", index=False)
        print '保存表格成功'

    if __name__ == "__main__":
        read_excel(file_path=file)
        mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com",]
        mail_title = 'Hey subject'
        mail_content = 'Hey this is content'
        mm = Mailer(mailto_list, mail_title, mail_content)
        res = mm.sendMail()
        print res
    return '调取信修A成功' + render_template('result.html')


@app.route("/send_code_B", methods=['POST'])
def send_codeB():
    upload_dir = r"C:\Python27\flask_test\diaozi1\upload"
    report_dir = r"C:\Python27\flask_test\diaozi1\result"
    lists = os.listdir(upload_dir)
    ##申明匿名函数 获取最新访问的文件
    lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
    print(lists[-1])
    # 获取最新的文件
    file = os.path.join(upload_dir, lists[-1])
    if (os.path.exists(report_dir))==False:
        os.mkdir(report_dir)

    def read_excel(file_path):
        file_df = pd.read_excel(file_path, names=['name', 'idcard', 'phone'])
        user_list = []
        resultnum = 0
        for idx, each_row in file_df.iterrows():
            _name = each_row["name"]
            _idcard = each_row["idcard"]
            _phone = each_row["phone"]
            url = 'http://10.76.11.20:82/api/services/cornucopia/hds?name=%s&idcard=%s&phone=%s&auth_org=hulushuju&max_query_time_interval=180&update=False' % (
                _name, _idcard, _phone)
            res = requests.get(url)
            data = json.loads(res.text)
            result = data.get("result", [])
            if result:
                ctc_lts = result.get("eb_dts", [])
                if ctc_lts:
                    for i in range(len(ctc_lts)):
                        ctc_lts[i]["uname"] = _name
                        ctc_lts[i]["idcard"] = _idcard
                        ctc_lts[i]["phoneNum"] = _phone
                        # phone1=ctc_lts[i]["eb_phone"]
                        # num_phone = phone1[:3] + "**" + phone1[5:]
                        # ctc_lts[i]["eb_phone"]=num_phone
                    user_list.extend(ctc_lts)
                    print(idx, each_row)

        opt_df = pd.DataFrame(user_list)
        opt_df.to_excel(result_dir+"/"+file_time+'B'+'.'+"xlsx", encoding="utf-8", index=False)

    if __name__ == "__main__":
        # main_run()
        read_excel(file_path=file)
        mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com", "zouchen@daihoubang.com","zouchen1983@163.com"]
        mail_title = 'Hey subject'
        mail_content = 'Hey this is content'
        mm = Mailer(mailto_list, mail_title, mail_content)
        res = mm.sendMail()
        print res
        print '保存表格成功'
    return '调取信修B成功' + render_template('result.html')


@app.route("/send_code_C", methods=['POST'])
def send_codeC():
    upload_dir = r"C:\Python27\flask_test\diaozi1\upload"
    report_dir = r"C:\Python27\flask_test\diaozi1\result"
    lists = os.listdir(upload_dir)
    ##申明匿名函数 获取最新访问的文件
    lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
    print(lists[-1])
    # 获取最新的文件
    file = os.path.join(upload_dir, lists[-1])
    if (os.path.exists(report_dir)) == False:
        os.mkdir(report_dir)
    def read_excel(file_path):
        frames = []
        file_df = pd.read_excel(file_path, names=['name', 'idcard', 'phone'])
        for idx, each_row in file_df.iterrows():
            _name = each_row["name"]
            _idcard = each_row["idcard"]
            _phone = each_row["phone"]
            url = 'http://10.76.11.20:82/api/services/cornucopia/huluwa?name=%s&idcard=%s&phone=%s&auth_org=hulushuju&max_query_time_interval=180&update=False' % (
                _name, _idcard, _phone)
            res = requests.get(url)
            data = json.loads(res.text)
            result = data.get("result", [])
            if result:
                result = formatData(result, "addr")
                result = formatData(result, "other_nm")
                result = formatData(result, "ct_ph")
                result = formatData(result, "ct_nm")
                result = formatData(result, "other_idcd")
                result = formatData(result, "other_ph")
                result = formatData(result, "co_nm")
                result = formatData(result, "email")
                result = formatData(result, "imp_ct_idcd")
                result = formatData(result, "eb_reciv_ph")
                result = formatData(result, "weibo")
                result = formatData(result, "ct_addr")
                frames.extend(result)
        opt_df = pd.DataFrame(frames)
        opt_df.to_excel(result_dir+"/"+file_time+'C'+'.'+"xlsx", encoding="utf-8", index=False)
        # print opt_df
        print '保存表格成功'

    def formatData(data, paramName):
        for i in range(len(data)):
            if len(data[i][paramName]) >= 0:
                for n in range(len(data[i][paramName])):
                    data[i]["%s_%s" % (paramName, n)] = data[i][paramName][n]
            data[i][paramName] = "空"
        return data
    if __name__ == "__main__":
        read_excel(file_path=file)
        mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com","zouchen@daihoubang.com"]
        mail_title = 'Hey subject'
        mail_content = 'Hey this is content'
        mm = Mailer(mailto_list, mail_title, mail_content)
        res = mm.sendMail()
        if os.path.exists(report_dir):
            shutil.rmtree(report_dir)
        print res
    return '调取信修C成功' + render_template('result.html')
@app.route("/clearresult", methods=['get'])
def clearresult():
    return render_template('calender.html')
@app.route("/clearresult1", methods=['POST'])
def clearresult1():
    datetime=request.form.get('datatime')
    bach_name=request.form.get('bach_name')
    # session['datetime']=datetime
    # print(session['datetime'])
    db_host = "10.76.2.2"
    # db_port=3306
    db_user = "admin_readonly"
    db_password = "Collect@2017#dhb"
    db_data = "collect"
    # port=db_port,
    file_time = time.strftime('%Y%m%d%S', time.localtime(time.time()))
    result_dir = r"C:\Python27\flask_test\diaozi1\result"
    lists = os.listdir(result_dir)
    ##申明匿名函数 获取最新访问的文件
    lists.sort(key=lambda fn: os.path.getatime(result_dir + '\\' + fn))
    file = os.path.join(result_dir, lists[-1])
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_data,charset="utf8")

    wb = xlwt.Workbook(encoding='utf-8')  # 创建一个excel工作簿，编码utf-8，表格中支持中文
    sheet = wb.add_sheet('sheet 1')  # 创建一个sheet
    cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)  # 创建一个指针对象
    # 查询SQL
    cursor.execute("SELECT t1.called_no,t1.feedback FROM soft_phone_clear_details_info t1 LEFT JOIN batch_info t2 ON t1.batch_id = t2.batch_id WHERE t1.create_date >= '%s'AND t1.feedback != ''AND t2.batch_name = '%s'"% (datetime,bach_name))

    results = cursor.fetchall()
    if results ==():
        print results
        return u"未找到对应批次数据！"
    else:

        # 获取查询结果
        columnName = []
        col = results[0].keys()

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
            "local_arrearage": "本机已欠费"

        }
        for i in range(0, rows):
            for j in range(columnLen):
                if (j == 0):
                    sheet.write(i + 1, j, results[i][columnName[j]])
                else:
                    sheet.write(i + 1, j, dict[results[i][columnName[j]]])

        if __name__ == '__main__':
            wb.save(result_dir + "/" + file_time + 'clear' + '.' + "xlsx")
            mailto_list = ["wangyue@daihoubang.com","zouchen@daihoubang.com"]
            mail_title = 'Hey subject'
            mail_content = 'Hey this is content'
            mm = Mailer(mailto_list, mail_title, mail_content)
            res = mm.sendMail()
            print res
            # 保存表格
            print '保存表格成功'
            cursor.close()
            db.close()
    return render_template('calender.html')
if __name__ == '__main__':
    app.run(port=5000,host='192.168.16.220',threaded=True)
