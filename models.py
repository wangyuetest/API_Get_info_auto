#encoding:utf-8
from exts import db
import datetime
class User(db.Model):
    __tablename__ ="user"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)  #unique代表不能重复，唯一的
    pwd = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(64),nullable=False)
    phone = db.Column(db.String(11),nullable=False,unique=True)
    face = db.Column(db.String(100))         #头像
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.now)
    updatetime=db.Column(db.DateTime,index=True,default=datetime.datetime.now)
    uuid = db.Column(db.String(255))


    def __repr__(self): #定义返回的类型
        return '<user %r>' % self.name

    def check_pwd(self,pwd):#验证密码
        from werkzeug.security import check_password_hash
        return  check_password_hash(self.pwd,pwd)

