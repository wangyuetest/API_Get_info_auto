#coding:utf-8
import time
import pandas as pd
import requests
import json
import config
import shutil
import pymysql
import xlwt, xlrd
import threading
from test_report_email_ import Mailer
from concurrent import futures
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
import sys
from sqlalchemy import create_engine
# reload(sys)
# sys.setdefaultencoding('utf8')
#windows下数据库连接
yconnect = create_engine('mysql://admin:UAT#2017admin@192.168.1.122/test?charset=utf8')
#centos下数据库连接
# yconnect = create_engine(mysql+pymysql://admin:UAT#2017admin@192.168.1.122/test?charset=utf8')
LOG_FORMAT="%(asctime)s=====+++++%(levelname)s++*****++%(message)s"
logging.basicConfig(filename="tsetdiaozi.log",level=logging.WARNING,format=LOG_FORMAT)
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
with app.app_context():
    # db.init()
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
        logging.error(jsonify)

@app.route("/login", methods=['GET','POST'])
def login():
    forms =LoginForm()#实例化forms
    if request.method=='POST'and forms.validate_on_submit(): #提交的时候进行验证,如果数据能被所有验证函数接受，则返回true，否则返回false
        data = forms.data#获取form数据信息（包含输入的用户名（account）和密码（pwd）等信息）,这里的account和pwd是在forms.py里定义的
        admin = User.query.filter_by(name=data["account"]).first()#查询表信息admin表里的用户名信息
        if admin == None:
            return  jsonify({"descraption":u"username is wrong!! ","errno": 1002, "errmsg": u"failed",})#操作提示信息，会在前端显示
        elif admin != None and not admin.check_pwd(data["pwd"]):      #这里的check_pwd函数在models 下Admin模型下定义
            return jsonify({"descraption":u"password is wrong!! ","errno": 1003, "errmsg": u"failed",})
        session['name']= data['account']#匹配成功，添加session
        db.session.commit()
        try:
          return redirect(request.args.get('next') or url_for('indexpage'))#重定向到下一页
        except Exception as e:
          logging.error(e)
          print(e)
        finally:
            session['name'] = data['account']  # 匹配成功，添加session
            return redirect(request.args.get('next') or url_for('indexpage'))  # 重定向到下一页

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

file_time=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
result_dir=r'C:\Python27\flask_test\diaozi1\result'
@app.route("/send_code_A", methods=['POST'])
def send_codeA():
    user_list = []
    json_list = []
    upload_dir = r'C:\Python27\flask_test\diaozi1\upload'
    lists = os.listdir(upload_dir)
    ##申明匿名函数 获取最新访问的文件
    lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
    print(lists[-1])
    # 获取最新的文件
    file = os.path.join(upload_dir, lists[-1])
    if (os.path.exists(result_dir))==False:
        os.mkdir(result_dir)
    def get_api(user_list, x):
        print ('start join:'+"第" + str(x) + "个线程" +file_time+"\n")
        y = 1
        for i in user_list:
            if y % 4 == x:
                url = 'http://10.76.11.20:82/api/services/cornucopia/rpt_ctc?name=%s&idcard=%s&phone=%s&auth_org=hulushuju' % (
                i['name'], i['idcard'], str(i['phone']))

                res = requests.get(url)
                data = json.loads(res.text)
                result = data.get("result", [])

                print(result)
                if result:
                    ctc_lts = result[0].get("contact_list", [])
                    if ctc_lts:
                        for j in range(len(ctc_lts)):
                            ctc_lts[j]["uname"] = i['name']
                            ctc_lts[j]["idcard"] = i['idcard']
                            ctc_lts[j]["phoneNum"] = i['phone']
                            # phlist = _phone[4:5]
                            # _newphone = _phone.replace(list, '**')
                            # print _newphone
                    json_list.extend(ctc_lts)
            y += 1
        if len(user_list)-1:
            print(len(user_list)-1)
            opt_df = pd.DataFrame(json_list)
            opt_df.to_excel(result_dir+"/"+file_time+'A'+'.'+"xlsx", encoding="utf-8", index=False)

    def procuder():
        file_df = pd.read_excel(file, names=['name', 'idcard', 'phone'])
        for idx, each_row in file_df.iterrows():
            if file_df.iterrows():
                name = each_row["name"]
                idcard = each_row["idcard"]
                phone = str(each_row["phone"])
                if phone.count('.')==1:
                    phone = str(each_row["phone"]).replace('.0', '')
            # user_list.extend((_name,_idcard,_phone))
            user_list.extend([{"name": name, "idcard": idcard, "phone": phone}])

        # print(user_list)
        return user_list

    def main():
        task=[]
        x = 0
        user_list = procuder()
        for i in user_list:
            print(i["name"])
        for x in range(4):
            th = threading.Thread(target=get_api, args=((user_list, x)))
            th.start()
            task.append(th)
            x += 1
        for tt in task:
            tt.join()
        print ('end join: '+"第" + str(x) + "个线程" +file_time+"\n")
    if __name__ == "__main__":
        main()
        mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com",]
        mail_title = 'Hey subject'
        mail_content = 'Hey this is content'
        mm = Mailer(mailto_list, mail_title, mail_content)
        if os.listdir(result_dir):
            res = mm.sendMail()
        print (res)
    return '调取信修A成功' + render_template('result.html')


@app.route("/send_code_B", methods=['POST'])
def send_codeB():
    user_list = []
    json_list = []
    result_dir = r'C:\Python27\flask_test\diaozi1\result'
    upload_dir = r'C:\Python27\flask_test\diaozi1\upload'
    lists = os.listdir(upload_dir)
    ##申明匿名函数 获取最新访问的文件
    lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
    print(lists[-1])
    # 获取最新的文件
    file = os.path.join(upload_dir, lists[-1])
    if (os.path.exists(result_dir)) == False:
        os.mkdir(result_dir)

    def get_api(user_list, x):
        y = 1
        print ('start join: ' + "第" + str(x) + "个线程" + file_time + "\n")
        for i in user_list:
            if y % 4 == x:
                print(i['name'])
                print(i['idcard'])
                print(i['phone'])
                print("第" + str(x) + "个线程")
                url = 'http://10.76.11.20:82/api/services/cornucopia/hds?name=%s&idcard=%s&phone=%s&auth_org=hulushuju&max_query_time_interval=180&update=False' % (
                    i['name'], i['idcard'], i['phone'])
                res = requests.get(url)
                data = json.loads(res.text)
                result = data.get("result", [])
                print(result)
                if result:
                    ctc_lts = result.get("eb_dts", [])
                    if ctc_lts:
                        for j in range(len(ctc_lts)):
                            ctc_lts[j]["uname"] = i['name']
                            ctc_lts[j]["idcard"] = i['idcard']
                            ctc_lts[j]["phoneNum"] = i['phone']
                            ctc_lts[j]["create_time"]=file_time
                            # phone1=ctc_lts[i]["eb_phone"]
                            # num_phone = phone1[:3] + "**" + phone1[5:]
                            # ctc_lts[i]["eb_phone"]=num_phone
                        json_list.extend(ctc_lts)
            y += 1
        opt_df = pd.DataFrame(json_list)
        try:
            if result['is_cache']:
                print(result['is_cache'])
                # opt_df.to_sql("test_diaozi", yconnect, if_exists='replace')
            else:
                opt_df.to_sql("test_diaozi", yconnect, if_exists='replace')
        except Exception as e:
            logging.error(e)
        finally:
            pass
        if len(user_list) - 1:
            print(len(user_list) - 1)
            opt_df = pd.DataFrame(json_list)
            opt_df.to_excel(result_dir + "/" + file_time + 'A' + '.' + "xlsx", encoding="utf-8", index=False)

    def procuder():
        file_df = pd.read_excel(file, names=['name', 'idcard', 'phone'])
        for idx, each_row in file_df.iterrows():
            if file_df.iterrows():
                name = each_row["name"]
                idcard = each_row["idcard"]
                phone = str(each_row["phone"])
                if phone.count('.') == 1:
                    phone = str(each_row["phone"]).replace('.0', '')
            # user_list.extend((_name,_idcard,_phone))
            user_list.extend([{"name": name, "idcard": idcard, "phone": phone}])

        # print(user_list)
        return user_list

    def main():
        task = []
        x = 0
        user_list = procuder()
        for i in user_list:
            print(i["name"])
        for x in range(4):
            th = threading.Thread(target=get_api, args=((user_list, x)))
            th.start()
            task.append(th)
            x += 1
        for tt in task:
            tt.join()
        print ('end join: ' + "第" + str(x) + "个线程" + file_time + "\n")

    if __name__ == "__main__":
        main()
        mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com", ]
        mail_title = 'Hey subject'
        mail_content = 'Hey this is content'
        mm = Mailer(mailto_list, mail_title, mail_content)
        if os.listdir(result_dir):
            res = mm.sendMail()
        print (res)
    return '调取信修B成功' + render_template('result.html')



@app.route("/send_code_C", methods=['POST'])
def send_codeC():
    user_list = []
    json_list = []
    result_dir = r'C:\Python27\flask_test\diaozi1\result'
    upload_dir = r'C:\Python27\flask_test\diaozi1\upload'
    lists = os.listdir(upload_dir)
    ##申明匿名函数 获取最新访问的文件
    lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
    print(lists[-1])
    # 获取最新的文件
    file = os.path.join(upload_dir, lists[-1])
    if (os.path.exists(result_dir)) == False:
        os.mkdir(result_dir)

    def get_api(user_list, x):
        print ('start join: ' + "第" + str(x) + "个线程" + file_time+ "\n")
        y = 1
        for i in user_list:
            if y % 4 == x:
                print(i['name'])
                print(i['idcard'])
                print(i['phone'])
                url = 'http://10.76.11.20:82/api/services/cornucopia/huluwa?name=%s&idcard=%s&phone=%s&auth_org=hulushuju&max_query_time_interval=180&update=False' % (
                    i['name'], i['idcard'], i['phone'])
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
                json_list.extend(result)
            y += 1
        if len(user_list) - 1:
            print(len(user_list) - 1)
            opt_df = pd.DataFrame(json_list)
            opt_df.to_excel(result_dir + "/" + file_time + 'A' + '.' + "xlsx", encoding="utf-8", index=False)
    def formatData(data, paramName):
        for j in range(len(data)):
            if len(data[j][paramName]) >= 0:
                for n in range(len(data[j][paramName])):
                    data[j]["%s_%s" % (paramName, n)] = data[j][paramName][n]
            data[j][paramName] = "空"
        return data

    def procuder():
        file_df = pd.read_excel(file, names=['name', 'idcard', 'phone'])
        for idx, each_row in file_df.iterrows():
            if file_df.iterrows():
                name = each_row["name"]
                idcard = each_row["idcard"]
                phone = str(each_row["phone"])
                if phone.count('.') == 1:
                    phone = str(each_row["phone"]).replace('.0', '')
            # user_list.extend((_name,_idcard,_phone))
            user_list.extend([{"name": name, "idcard": idcard, "phone": phone}])

        # print(user_list)
        return user_list

    def main():
        task = []
        x = 0
        user_list = procuder()
        for i in user_list:
            print(i["name"])
        for x in range(4):
            th = threading.Thread(target=get_api, args=((user_list, x)))
            th.start()
            task.append(th)
            x += 1
        for tt in task:
            tt.join()
        print ('end join: ' + "第" + str(x) + "个线程" + file_time + "\n")


    if __name__ == "__main__":
        main()
        mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com", ]
        mail_title = 'Hey subject'
        mail_content = 'Hey this is content'
        mm = Mailer(mailto_list, mail_title, mail_content)
        if os.listdir(result_dir):
            res = mm.sendMail()
        print (res)
    return '调取信修C成功' + render_template('result.html')
@app.route("/clearresult", methods=['get'])
def clearresult():
    return render_template('calender.html')
@app.route("/clearresult", methods=['POST'])
def clearresult1():
    a=[]
    starttime=request.form.get('starttime')
    endtime=request.form.get('endtime')
    called_phone=request.form.get('called_phone')
    # session['datetime']=datetime
    # print(session['datetime'])
    db_host = "10.76.2.2"
    # db_port=3306
    db_user = "admin_readonly"
    db_password = "Collect@2017#dhb"
    db_data = "collect"
    # port=db_port,
    file_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    report_dir = r'C:\Python27\flask_test\diaozi1\record'
    # lists = os.listdir(report_dir)
    ##申明匿名函数 获取最新访问的文件
    # lists.sort(key=lambda fn: os.path.getatime(report_dir + '\\' + fn))
    # # 获取最新的文件
    # file = os.path.join(report_dir, lists[-1])
    db = pymysql.connect(host=db_host, user=db_user, passwd=db_password, db=db_data,charset="utf8")

    # wb = xlwt.Workbook(encoding='utf-8')  # 创建一个excel工作簿，编码utf-8，表格中支持中文
    # sheet = wb.add_sheet('sheet 1')  # 创建一个sheet
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)  # 创建一个指针对象
    # 查询SQL
    j = 0
    if starttime and endtime and called_phone:
        mySql = "SELECT * FROM  collect_soft_phone_event WHERE create_date > '%s'AND create_date<'%s'AND called_no='%s'" % (
        starttime, endtime, called_phone)
        cursor.execute(mySql)
        print(mySql)
        results = cursor.fetchall()
        if results:
            for i in results:
                record_file=i['record_file']
                if record_file:
                    a.append(record_file)
                    j += 1
            opt_df = pd.DataFrame(a)
        else:
            jsonify({"descraption": "没有查询对应的录音"})

    elif called_phone:
        Sql = "SELECT * FROM  collect_soft_phone_event WHERE called_no='%s'" % (called_phone)
        cursor.execute(Sql)
        print(Sql)
        results = cursor.fetchall()
        if results:
            for i in results:
                record_file = i['record_file']
                if record_file:
                    a.append(record_file)
                    j += 1

            opt_df = pd.DataFrame(a)
        else:
            jsonify({"descraption": "没有查询对应的录音"})
    else:
       return "未查到数据！请输入查询信息"
        # opt_df.to_sql("test_records", yconnect, if_exists='replace')

    if __name__ == '__main__':
        try:
         opt_df.to_excel((report_dir + "/" + file_time + 'record' + '.' + "xlsx"))
        except Exception as e:
            pass

    print(j)
    return render_template('calender.html',url=a,status=j,time=create_time)

if __name__ == '__main__':
   app.run(port=5000,host='0.0.0.0',threaded=True)
