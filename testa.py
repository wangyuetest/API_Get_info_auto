# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
import os
import re
from test_report_email_ import *


# import re
#
# phone = "13883438573 # 这是一个国外电话号码"
#
# # 删除字符串中的 Python注释
# num = re.sub(r'#.*$', "", phone)
# print "电话号码是: ", num
#
# # 删除非数字(-)的字符串
# num = re.sub(r'\d(4)', "**", phone)
# print "电话号码是 : ", num


import threading
from time import ctime,sleep


def music(func):
    for i in range(2):
        def send_codeB(func):
            upload_dir = './upload'
            lists = os.listdir(upload_dir)
            ##申明匿名函数 获取最新访问的文件
            lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
            print(lists[-1])
            # 获取最新的文件
            file = os.path.join(upload_dir, lists[-1])

            def read_excel(file_path):
                resultnum = 0
                file_df = pd.read_excel(file_path, names=['name', 'idcard', 'phone'])
                user_list = []
                for idx, each_row in file_df.iterrows():
                    _name = each_row["name"]
                    _idcard = each_row["idcard"]
                    _phone = each_row["phone"]
                    url = 'http://10.76.11.20:82/api/services/cornucopia/rpt_ctc?name=%s&idcard=%s&phone=%s&auth_org=hulushuju' \
                          % (_name, _idcard, _phone)
                    res = requests.get(url)
                    data = json.loads(res.text)
                    result = data.get("result", [])
                    # print idx, _name, _idcard, _phone
                    if result:
                        ctc_lts = result[0].get("contact_list", [])
                        if ctc_lts:
                            for i in range(len(ctc_lts)):
                                ctc_lts[i]["uname"] = _name
                                ctc_lts[i]["idcard"] = _idcard
                                ctc_lts[i]["phoneNum"] = _phone
                        user_list.extend(ctc_lts)
                        resultnum += 1
                print resultnum
                opt_df = pd.DataFrame(user_list)
                opt_df.to_excel("data2c.xlsx", encoding="utf-8", index=False)
                print '保存表格成功'

            if __name__ == "__main__":
                # main_run()
                read_excel(file_path=file)
                mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com"]
                mail_title = 'Hey subject'
                mail_content = 'Hey this is content'
                mm = Mailer(mailto_list, mail_title, mail_content)
                res = mm.sendMail()
                print res

        print ("I was listening to %s. %s" %(func,ctime()))
        sleep(1)

def move(func):
    for i in range(2):
        print ("I was at the %s! %s" %(func,ctime()))
        sleep(5)

threads = []
t1 = threading.Thread(target=music,args=(u'测试开始',))
threads.append(t1)
t2 = threading.Thread(target=move,args=(u'阿凡达',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

    print("all over %s" %ctime())