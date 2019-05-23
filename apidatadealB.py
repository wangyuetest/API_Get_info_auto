# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
from test_report_email_ import *
import threading
from sqlalchemy import create_engine
from flask import Flask,render_template,jsonify,request,session,redirect,url_for,flash
#windows下数据库连接
yconnect = create_engine('mysql://admin:UAT#2017admin@192.168.1.122/test?charset=utf8')
app = Flask(__name__)
file_time =time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
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
        for i in user_list:
            if y % 4 == x:
                print(i['name'])
                print(i['idcard'])
                print(i['phone'])
                print("第" + str(x) + "个线程")
                url = 'http://10.76.11.20:82/api/services/cornucopia/hds?name=%s&idcard=%s&phone=%s&auth_org=hulushuju&max_query_time_interval=180&update=False'  % (
                    i['name'], i['idcard'], i['phone'])
                res = requests.get(url)
                data = json.loads(res.text)
                result = data.get("result", [])

                print(result)
                result = data.get("result", [])
                if result:
                    ctc_lts = result.get("eb_dts", [])
                    if ctc_lts:
                        for i in range(len(ctc_lts)):
                            ctc_lts[i]["uname"] =i['name']
                            ctc_lts[i]["idcard"] = i['idcard']
                            ctc_lts[i]["phoneNum"] =i['phone']
                            # phone1=ctc_lts[i]["eb_phone"]
                            # num_phone = phone1[:3] + "**" + phone1[5:]
                            # ctc_lts[i]["eb_phone"]=num_phone
                        json_list.extend(ctc_lts)
            opt_df = pd.DataFrame(json_list)
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
        opt_df.to_excel(result_dir + "/" + file_time + 'A' + '.' + "xlsx", encoding="utf-8", index=False)

    def procuder():
        file_df = pd.read_excel(file, names=['name', 'idcard', 'phone'])
        for idx, each_row in file_df.iterrows():
            if file_df.iterrows():
                name = each_row["name"]
                idcard = each_row["idcard"]
                phone = each_row["phone"]
            # user_list.extend((_name,_idcard,_phone))
            user_list.extend([{"name": name, "idcard": idcard, "phone": phone}])

        # print(user_list)
        return user_list

    def main():
        x = 0
        user_list = procuder()
        for i in user_list:
            print(i["name"])
        for x in range(4):
            th = threading.Thread(target=get_api, args=((user_list, x)))
            th.start()
            x += 1

    if __name__ == "__main__":
        main()
        mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com", ]
        mail_title = 'Hey subject'
        mail_content = 'Hey this is content'
        mm = Mailer(mailto_list, mail_title, mail_content)
        res = mm.sendMail()
        print (res)
    return '调取信修B成功' + render_template('result.html')
if __name__ == '__main__':

   app.run(port=5000,host='0.0.0.0',threaded=True)