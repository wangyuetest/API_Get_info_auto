# -*- coding: utf-8 -*-
import pandas as pd
import requests
import json
import os
# import threading
# from test_report_email_ import *
# # #全局锁
# # gLock = threading.Lock()
# upload_dir=r'C:\Python27\flask_test\diaozi1\upload'
# lists=os.listdir(upload_dir)
# ##申明匿名函数 获取最新访问的文件
# lists.sort(key=lambda fn:os.path.getatime(upload_dir+'\\'+fn) )
# print(lists[-1])
# #获取最新的文件
# file=os.path.join(upload_dir,lists[-1])
# user_list = []
# json_list = []
# # def read_excel(user_list,x):
# #     file_df= pd.read_excel(file,names=['name','idcard','phone'])
# #     for idx, each_row in file_df.iterrows():
# #         _name = each_row["name"]
# #         _idcard = each_row["idcard"]
# #         _phone = each_row["phone"]
# #         gLock.acquire()
# #         url = 'http://10.76.11.20:82/api/services/cornucopia/rpt_ctc?name=%s&idcard=%s&phone=%s&auth_org=hulushuju' % (
# #         _name, _idcard, _phone)
# #         res = requests.get(url)
# #         gLock.release()
# #         data = json.loads(res.text)
# #         result = data.get("result", [])
# #         if result:
# #             ctc_lts = result[0].get("contact_list", [])
# #             if ctc_lts:
# #                 for i in range(len(ctc_lts)):
# #                     ctc_lts[i]["uname"] = _name
# #                     ctc_lts[i]["idcard"] = _idcard
# #                     ctc_lts[i]["phoneNum"] = _phone
# #                     # phlist = _phone[4:5]
# #                     # # _newphone = _phone.replace(list, '**')
# #                     # # print _newphone
# #             user_list.extend(ctc_lts)
# #     opt_df = pd.DataFrame(user_list)
# #     opt_df.to_excel(r"C:\Python27\flask_test\diaozi1\result\dataA.xlsx", encoding="utf-8", index=False)
#
#
# def get_api(user_list,x):
#     y=1
#     for i in user_list:
#         if y%4==x:
#             print(i['name'])
#             print(i['idcard'])
#             print(i['phone'])
#             print("第" + str(x) + "个线程")
#             url = 'http://10.76.11.20:82/api/services/cornucopia/rpt_ctc?name=%s&idcard=%s&phone=%s&auth_org=hulushuju'% (i['name'],i['idcard'],i['phone'])
#
#             res = requests.get(url)
#             data = json.loads(res.text)
#             result = data.get("result", [])
#
#             print(result)
#             if result:
#                 ctc_lts = result[0].get("contact_list", [])
#                 if ctc_lts:
#                     for j in range(len(ctc_lts)):
#                         ctc_lts[j]["uname"] =i['name']
#                         ctc_lts[j]["idcard"] = i['idcard']
#                         ctc_lts[j]["phoneNum"] = i['phone']
#                         # phlist = _phone[4:5]
#                         # _newphone = _phone.replace(list, '**')
#                         # print _newphone
#                 json_list.extend(ctc_lts)
#         y += 1
#     opt_df = pd.DataFrame(json_list)
#     opt_df.to_excel(r"C:\Python27\flask_test\diaozi1\result\dataA.xlsx", encoding="utf-8", index=False)
#
#
# def procuder():
#       file_df = pd.read_excel(file, names=['name', 'idcard', 'phone'])
#       for idx, each_row in file_df.iterrows():
#            if file_df.iterrows():
#               name = each_row["name"]
#               idcard = each_row["idcard"]
#               phone = each_row["phone"]
#            # user_list.extend((_name,_idcard,_phone))
#            user_list.extend([{"name":name,"idcard":idcard,"phone":phone}])
#
#
#       print(user_list)
#       return user_list
#
#
# def main():
#     x=0
#     user_list=procuder()
#     for i in user_list :
#         print(i["name"])
#     for x in range(4):
#         th = threading.Thread(target=get_api,args=((user_list,x)))
#         th.start()
#         x+=1
#
#
#
#
# if __name__ == "__main__":
#     # main_run()
    # procuder()
    # main()
    # # read_excel(file_path=file)
    # mailto_list = ["wangyue@daihoubang.com"]
    # mail_title = 'Hey subject'
    # mail_content = 'Hey this is content'
    # mm = Mailer(mailto_list, mail_title, mail_content)
    # res = mm.sendMail()
    # print res

import os
def search(path):
  files=os.listdir(path)   #查找路径下的所有的文件夹及文件
  for filee in  files:
      f=str(path+filee)    #使用绝对路径
      if os.path.isdir(f):  #判断是文件夹还是文件
        if not os.listdir(f):  #判断文件夹是否为空
          print(str(filee))
      else:
        print('f',f)
