# # encoding=utf-8
# import pandas as pd
# import requests
# import json
# import os
#
# user_list = []
# json_list = []
# result_dir = r'C:\Python27\flask_test\diaozi1\result'
# upload_dir = r'C:\Python27\flask_test\diaozi1\upload'
# lists = os.listdir(upload_dir)
# ##申明匿名函数 获取最新访问的文件
# lists.sort(key=lambda fn: os.path.getatime(upload_dir + '\\' + fn))
# print(lists[-1])
# # 获取最新的文件
# file = os.path.join(upload_dir, lists[-1])
# if (os.path.exists(result_dir)) == False:
#     os.mkdir(result_dir)
# def get_api(user_list, x):
#     y = 1
#     for i in user_list:
#         if y % 4 == x:
#             print(i['name'])
#             print(i['idcard'])
#             print(i['phone'])
#             print("第" + str(x) + "个线程")
#             url = 'http://10.76.11.20:82/api/services/cornucopia/huluwa?name=%s&idcard=%s&phone=%s&auth_org=hulushuju&max_query_time_interval=180&update=False' % (
#                 i['name'], i['idcard'], i['phone'])
#             res = requests.get(url)
#             data = json.loads(res.text)
#             result = data.get("result", [])
#
#             print(result)
#             result = data.get("result", [])
#             if result:
#                 result = formatData(result, "addr")
#                 result = formatData(result, "other_nm")
#                 result = formatData(result, "ct_ph")
#                 result = formatData(result, "ct_nm")
#                 result = formatData(result, "other_idcd")
#                 result = formatData(result, "other_ph")
#                 result = formatData(result, "co_nm")
#                 result = formatData(result, "email")
#                 result = formatData(result, "imp_ct_idcd")
#                 result = formatData(result, "eb_reciv_ph")
#                 result = formatData(result, "weibo")
#                 result = formatData(result, "ct_addr")
#                 json_list.extend(result)
#         y += 1
#     opt_df = pd.DataFrame(json_list)
#     opt_df.to_excel(result_dir + "/" + file_time + 'C' + '.' + "xlsx", encoding="utf-8", index=False)
#  def formatData(data, paramName):
#         for i in range(len(data)):
#             if len(data[i][paramName]) >= 0:
#                 for n in range(len(data[i][paramName])):
#                     data[i]["%s_%s" % (paramName, n)] = data[i][paramName][n]
#             data[i][paramName] = "空"
#         return data
#
# def procuder():
#     file_df = pd.read_excel(file, names=['name', 'idcard', 'phone'])
#     for idx, each_row in file_df.iterrows():
#         if file_df.iterrows():
#             name = each_row["name"]
#             idcard = each_row["idcard"]
#             phone = each_row["phone"]
#         # user_list.extend((_name,_idcard,_phone))
#         user_list.extend([{"name": name, "idcard": idcard, "phone": phone}])
#
#     # print(user_list)
#     return user_list
#
#
# def main():
#     x = 0
#     user_list = procuder()
#     for i in user_list:
#         print(i["name"])
#     for x in range(4):
#         th = threading.Thread(target=get_api, args=((user_list, x)))
#         th.start()
#         x += 1
#
#
# if __name__ == "__main__":
#     main()
#     mailto_list = ["wangyue@daihoubang.com", "975405349@qq.com", ]
#     mail_title = 'Hey subject'
#     mail_content = 'Hey this is content'
#     mm = Mailer(mailto_list, mail_title, mail_content)
#     res = mm.sendMail()
#     print (res)
# return '调取信修C成功' + render_template('result.html')
#
