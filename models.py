# -- coding: utf-8 --
import datetime
from config import  SECRET_KEY  
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
db = SQLAlchemy()

#用户表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    userId=db.Column(db.String(255),nullable=False)
    creatTime=db.Column(db.String(255),nullable=False)
    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)
    
    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间1天
    def generate_auth_token(self, expiration = 60*60*24):
        s = Serializer(SECRET_KEY, expires_in = expiration)
        return s.dumps({ 'token': self.userId })

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['userId'])
        return user

#地址表
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userId = db.Column(db.String(255),nullable=False)
    ContactPerson = db.Column(db.String(255),nullable=False)
    ContactNumber = db.Column(db.String(255),nullable=False)
    ContactAddress = db.Column(db.String(255),nullable=False)
    ContactDetailAddress = db.Column(db.String(255),nullable=False)
    AddressId = db.Column(db.String(255),nullable=False)
    isDefault = db.Column(db.Integer,nullable=False)


#商品表
class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    goodsId = db.Column(db.String(255),nullable=False)
    goodsName = db.Column(db.String(255),nullable=False)
    goodsImgArr = db.Column(db.Text,nullable=False)
    goodsPrice = db.Column(db.String(255),nullable=False)
    TopCategoryId = db.Column(db.String(255),nullable=False)
    SecondaryCategoryId = db.Column(db.Integer,nullable=False)
    ThirdCategoryId = db.Column(db.String(255),nullable=False)
    goodsSize = db.Column(db.String(255),nullable=False)

#购物车表
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userId = db.Column(db.String(255),nullable=False)
    goodsId = db.Column(db.String(255),nullable=False)
    goodsPrice = db.Column(db.String(255),nullable=False)
    goodsNumber = db.Column(db.String(255),nullable=False)
    goodsStyle = db.Column(db.String(255),nullable=False)
    goodsSize = db.Column(db.String(255),nullable=False)  


#订单表
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userId = db.Column(db.String(255),nullable=False)
    orderId = db.Column(db.String(255),nullable=False)
    orderType = db.Column(db.String(255),nullable=False) 
    goodsId = db.Column(db.String(255),nullable=False)
    addressId = db.Column(db.String(255),nullable=False) 
    goodsNumber = db.Column(db.String(255),nullable=False)
    goodsStyle = db.Column(db.String(255),nullable=False)
    goodsSize = db.Column(db.String(255),nullable=False) 
    remark = db.Column(db.String(255),nullable=False)
    createTime = db.Column(db.String(255),nullable=False)
    orderNo = db.Column(db.String(255),nullable=False)
    
  

#收藏表
class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userId = db.Column(db.String(255),nullable=False)
    goodsId = db.Column(db.String(255),nullable=False)
    collectId = db.Column(db.String(255),nullable=False) 
    
#系统优惠券表
class Coupon(db.Model):
    __tablename__ = 'coupon'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    couponId = db.Column(db.String(255),nullable=False)
    spendMoney = db.Column(db.String(255),nullable=False)
    disCount = db.Column(db.String(255),nullable=False)
    endTime = db.Column(db.String(255),nullable=False)
    title = db.Column(db.String(255),nullable=False)

#用户优惠券表
class UserCoupon(db.Model):
    __tablename__ = 'usercoupon'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userId = db.Column(db.String(255),nullable=False)
    couponId = db.Column(db.String(255),nullable=False)
   

#精选表
class Chosen(db.Model):
    __tablename__ = 'chosen'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    goodsId = db.Column(db.String(255),nullable=False)

#折扣表
class Discount(db.Model):
    __tablename__ = 'discount'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    goodsId = db.Column(db.String(255),nullable=False)
    discount = db.Column(db.String(255),nullable=False)

    
    


   
         

        