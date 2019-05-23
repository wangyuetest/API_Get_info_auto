#coding:utf-8
from flask_script import Manager
from main import app
from  flask_migrate import Migrate,MigrateCommand
from exts import db
#导入需要迁移的数据库模型
from models import User

manager=Manager(app)
#使用migrate,必须绑定APP和db
migrate=Migrate(app,db)
#把MigrateCommand命令添加到manager中
manager.add_command('db',MigrateCommand)

# 初始化
#
# (venv) python manage.py db init
# 创建迁移脚本
#
# (venv) python manage.py db migrate
# 更新数据库
#
# (venv) python  manage.py db upgrade


if __name__=="__main__":
    manager.run()
