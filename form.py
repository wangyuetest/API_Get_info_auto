#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask_wtf import FlaskForm                 #FlaskForm 为表单基类
from wtforms import StringField,PasswordField,SubmitField     #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo
from models import User
class RegisterForm(FlaskForm):
    account = StringField(
        # 标签
        label="用户名",
        # 验证器
        validators=[
            DataRequired('请输入用户名')
        ],
        description="用户名",
        # 附加选项,会自动在前端判别
        render_kw={
            "placeholder":"请输入用户名",
            "required":'required'               #表示输入框不能为空
        }
    )

    email = StringField(
        label="邮箱",
        # 验证器
        validators=[
            DataRequired('请输入邮箱'),
            Email('邮箱格式不正确')
        ],
        description="邮箱",
        # 附加选项,会自动在前端判别
        render_kw={
            "placeholder": "请输入邮箱!",
           "required": 'required' # 表示输入框不能为空
        }
    )

    phone = StringField(
        label="手机",
        # 验证器
        validators=[
            DataRequired('请输入手机号码'),
            Regexp("1[3578]\d{9}", message="手机格式不正确")# 用正则匹配手机号码规则
        ],
        description="手机",
        # 附加选项,会自动在前端判别
        render_kw={
            "placeholder": "请输入手机号码",
            "required": 'required'# 表示输入框不能为空
        }
    )

    pwd = PasswordField(
        # 标签
        label="密码",
        # 验证器
        validators=[
            DataRequired('请输入密码')
        ],
        description="密码",
        # 附加选项,会自动在前端判别
        render_kw={

            "placeholder": "请输入密码!",
            "required": 'required'  # 表示输入框不能为空
        }
    )

    repwd = PasswordField(
        # 标签
        label="确认密码",
        # 验证器
        validators=[
            DataRequired('确认密码'),
            EqualTo('pwd',message="两次密码输入不一致")
        ],
        description="确认密码",
        # 附加选项,会自动在前端判别
        render_kw={
            "placeholder": "确认密码",
            "required": 'required'  # 表示输入框不能为空
        }
    )
    submit = SubmitField(
        label="注册",
        render_kw={
            "class": "btn btn-success btn-block",
        }
    )

    # 账号认证，自定义验证器，判断输入的值是否唯一
    def validate_name(self, filed):
        name = filed.data
        account = User.query.filter_by(username=name).count()
        if account == 1:
            raise ValidationError("昵称已经存在")

    def validate_email(self, filed):
        emails = filed.data
        account = User.query.filter_by(email=emails).count()
        if account == 1:
            raise ValidationError("邮箱已经注册")

    def validate_phone(self, filed):
        phones = filed.data
        account = User.query.filter_by(phone=phones).count()
        if account == 1:
            raise ValidationError("手机号已经注册")