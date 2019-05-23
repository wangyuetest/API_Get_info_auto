#coding:utf-8
import pandas as pd
import requests
def read_excel(file_path):
    file_df= pd.read_excel(file_path)
    for idx, each_row in file_df.iterrows():
        phone = each_row["phone"]
        header={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        url='http://118.178.138.170/msg/HttpBatchSendSM'
        data={
            "account":"zu7gtd",
            "pswd":"xVO7oX7T",
            "mobile":phone,
            "msg":"【这儿借】感谢您的接听！如需更多资讯，请关注微信公众号“这儿借”",
            "needstarus":"true",
            "resptype":"json"
        }
        print phone
        res = requests.post(url,data)
        print(res.status_code)
        print(res.text)

if __name__ == "__main__":
    # main_run()
    read_excel(file_path=r'C:\Users\ps\Desktop\zheerjie.xlsx')
