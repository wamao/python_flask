
# -- coding: utf-8 --
from flask import Flask
from flask import jsonify
from flask_cors import *
from flask import request
from models import User,db,Address,Cart,Coupon,UserCoupon,Collect,Goods
from passlib.apps import custom_app_context
import uuid
import time
import config  # 配置文件
from config import  UPLOAD_FOLDER,ALLOWED_EXTENSIONS 
from werkzeug import secure_filename
from sqlalchemy import and_
import os
import sys
import json
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)



app = Flask(__name__)
#处理跨域请求
CORS(app, supports_credentials=True)
#配置
app.config.from_object(config)
db.init_app(app)

class AlchemyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # 判断是否是Query
        if isinstance(obj, Query):
            # 定义一个字典数组
            fields = []
            # 定义一个字典对象
            record = {}
            # 检索结果集的行记录
            for rec in obj.all():
                # 检索记录中的成员
                for field in [x for x in dir(rec) if
                              # 过滤属性
                              not x.startswith('_')
                              # 过滤掉方法属性
                              and hasattr(rec.__getattribute__(x), '__call__') == False
                              # 过滤掉不需要的属性
                              and x != 'metadata']:
                    data = rec.__getattribute__(field)
                    try:
                        record[field] = data
                    except TypeError:
                        record[field] = None
                fields.append(record)
            # 返回字典数组
            return fields
        # 其他类型的数据按照默认的方式序列化成JSON
        return json.JSONEncoder.default(self, obj)     

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    
    # 返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}
    }
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if user and user.verify_password(password):
           responseData["status"]=0 
           Token=user.generate_auth_token() # 获取token
           responseData["result"]["Token"]=Token
           responseData["message"]="登录成功"
        else:
            responseData["status"]=1 
            responseData["message"]="用户名或密码错误"
    return jsonify(responseData)


# 用户注册
@app.route('/register',methods=["POST"])
def register():
    # 返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}
    }

    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        rspassword=request.form.get("rspassword")
        if not(username and password and rspassword):
            responseData["message"]="缺少业务参数"
        else:
            user = User.query.filter(User.username == username).first() 
            if user:
                 responseData["status"]=1 
                 responseData["message"]="该用户名已经被注册,换个用户名试试!"
            else:
                if password!=rspassword:
                    responseData["status"]=2 
                    responseData["message"]="两次密码输入不一致,请重新输入!"
                else:
                    creatTime=time.strftime("%Y-%m-%d %H:%M:%S")
                    userId=str(uuid.uuid1())
                    user = User(username=username,password=password,creatTime=creatTime,userId=userId)
                    user.hash_password(password)
                    db.session.add(user)
                    db.session.commit() 
                    responseData["status"]=0 
                    responseData["message"]="注册成功!"
    # 返回数据                
    return jsonify(responseData)

#添加用户地址
@app.route('/AddAddress',methods=["POST"])
def addaddress():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}
    }
    if request.method=="POST":
        ContactPerson=request.form.get("ContactPerson")    
        ContactNumber=request.form.get("ContactNumber")
        ContactAddress=request.form.get("ContactAddress")
        ContactDetailAddress=request.form.get("ContactDetailAddress")
        isDefault=request.form.get("isDefault")
        AddressId=str(uuid.uuid1())
        if not all([ContactPerson, ContactNumber , ContactAddress ,ContactDetailAddress] ) :
            responseData["status"]=1 
            responseData["message"]="缺少必要的业务参数!"
        else:
            address = Address(AddressId=AddressId,ContactPerson=ContactPerson,ContactNumber=ContactNumber,ContactAddress=ContactAddress,ContactDetailAddress=ContactDetailAddress,isDefault=isDefault)
            db.session.add(address)
            db.session.commit() 
            responseData["status"]=0 
            responseData["message"]="添加地址成功!"

    # 返回数据                
    return jsonify(responseData)


#获取用户地址
@app.route('/getAddress',methods=["POST"])
def getaddress():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{
            "addressList"
        }
    }
    addressList =Address.query.filter(Cart.userId == userId).all()
    responseData["status"]=0 
    responseData["message"]="获取用户地址成功!"
    responseData["result"]=jsonify(cartList)
   
    # 返回数据                
    return jsonify(context)  




#修改用户地址
@app.route('/editAddress',methods=["POST"])
def editAddress():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}  
    }

    ContactPerson=request.form.get("ContactPerson")    
    ContactNumber=request.form.get("ContactNumber")
    ContactAddress=request.form.get("ContactAddress")
    ContactDetailAddress=request.form.get("ContactDetailAddress")
    isDefault=request.form.get("isDefault")
    AddressId=request.form.get("AddressId")
   
    if not all([ContactPerson , ContactNumber, ContactAddress, ContactDetailAddress ,AddressId] ) :
            responseData["status"]=1 
            responseData["message"]="缺少必要的业务参数!"
    else:
        addressDetail = Address.query.filter(Address.AddressId == AddressId).first()
        addressDetail.ContactPerson=ContactPerson
        addressDetail.ContactNumber=ContactNumber
        addressDetail.ContactDetailAddress=ContactDetailAddress
        addressDetail.isDefault=isDefault 
        db.session.add(addressDetail)
        db.session.commit() 
        responseData["status"]=0 
        responseData["message"]="修改地址成功!" 

    # 返回数据                
    return jsonify(responseData)


#删除用户地址
@app.route('/delAddress',methods=["POST"])
def delAddress():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}  
    }
    AddressId=request.form.get("AddressId")
    if not  AddressId:
        responseData["status"]=1 
        responseData["message"]="缺少必要的业务参数!" 
    else:  
        address = Address.query.filter(Address.AddressId == AddressId).first()
        if not address:
           responseData["status"]=1 
           responseData["message"]="该地址不存在,删除失败!" 
        else:
            db.session.delete(address)
            db.session.commit()
            responseData["status"]=0 
            responseData["message"]="删除成功!"

    # 返回数据                
    return jsonify(responseData)



#设置默认地址
@app.route('/defaultAddress',methods=["POST"])
def defaultAddress():
    #返回参数结构
    responseData={
       "status":0,
       "message":'',
       "result":{}  
    }
    AddressId=request.form.get("AddressId")
    userId="111"
    if not AddressId:
        responseData["status"]=1 
        responseData["message"]="缺少必要的业务参数!"
    else:
        address = Address.query.filter(Address.userId == userId).all()
        for item in address:
            if item.AddressId==AddressId:
                item.isDefault=1
            else:
                item.isDefault=0 
            db.session.add(item)
        db.session.commit() 
        responseData["status"]=0 
        responseData["message"]="设置默认地址成功!"

    # 返回数据                
    return jsonify(responseData)

#加入购物车
@app.route('/addCart',methods=["POST"])
def addCart():
    #返回参数结构
    responseData={
       "status":0,
       "message":'',
       "result":{}  
    }
    goodsId = request.form.get("goodsId")
    goodsPrice = request.form.get("goodsPrice")
    goodsNumber = request.form.get("goodsNumber")
    goodsStyle =request.form.get("goodsStyle")
    goodsSize = request.form.get("goodsSize")
    userId='1111'
    if not ( goodsId and goodsPrice and goodsNumber and goodsStyle and goodsSize ):
        responseData["status"]=1 
        responseData["message"]="缺少必要的业务参数!"
    else:
        goods = Cart(goodsId=goodsId,goodsPrice=goodsPrice,goodsNumber=goodsNumber,goodsStyle=goodsStyle,goodsSize=goodsSize,userId=userId)
        db.session.add(goods)
        db.session.commit() 
        responseData["status"]=0 
        responseData["message"]="加入购物车成功!"

    # 返回数据                
    return jsonify(responseData)

#从购物车删除商品
@app.route('/delCart',methods=["POST"])
def delCart():
    #返回参数结构
    responseData={
       "status":0,
       "message":'',
       "result":{}  
    }
    
    goodsId = request.form.get("goodsId")
    userId='2222'
    if not goodsId:
        responseData["status"]=1 
        responseData["message"]="缺少必要的业务参数!"
    else:
        goods = Cart.query.filter(and_(Cart.userId == userId,Cart.userId == userId)).first()
        if not goods:
            responseData["status"]=1 
            responseData["message"]="删除失败,请稍后重试!" 
        else:    
            db.session.delete(goods)
            db.session.commit()
            responseData["status"]=0 
            responseData["message"]="删除商品成功!"

    # 返回数据                
    return jsonify(responseData)


#获取用户购物车商品
@app.route('/getCart',methods=["POST"])
def getCart():
    #返回参数结构
    responseData={
       "status":0,
       "message":'',
       "result":[]
    }
    
    userId='1111'
    arr=[]
    cartList = Cart.query.filter(Cart.userId == userId).all()
    arr=json.dumps(cartList, cls=AlchemyJsonEncoder)
    print arr
    responseData["status"]=0 
    responseData["message"]="获取购物车商品成功!"
    #responseData["result"]=arr
    context = {
        'questions':'sssss'
    }  
    # 返回数据                
    return jsonify(context) 



#商品分类查询
@app.route('/category',methods=["POST"])
def category():
    #返回参数结构
    responseData={
       "status":0,
       "message":'',
       "result":[]
    }

    return jsonify(responseData)


#查询商品详情
@app.route('/goodsDetail',methods=["POST"])
def goodsDetail():
    #返回参数结构
    responseData={
       "status":0,
       "message":'',
       "result":[]
    }

    goodsId = request.form.get("goodsId")
    cartList = Cart.query.filter(Cart.userId == userId).all()
    print cartList
    responseData["status"]=0 
    responseData["message"]="获取购物车商品成功!"
    # responseData["result"]=jsonify(cartList)
    context = {
        'questions':'sssss'
    }  
    # 返回数据                
    return jsonify(context)

    return jsonify(responseData)

#检查扩展名是否合法
def allowed_file(filename):
    isCheck='.' in filename and   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    return isCheck
     

#上传用户头像
@app.route('/uploadFile',methods=["POST"])
def uploadFile():
    #返回参数结构
    responseData={
       "status":0,
       "message":'',
       "result":{}
    }
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            responseData["status"]=0 
            responseData["message"]="文件上传成功!"
        else:
            responseData["status"]=1 
            responseData["message"]="文件上传格式不正确!"
    return jsonify(responseData) 


#添加系统优惠券
@app.route('/addCoupon',methods=["POST"])
def addCoupon():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}
    }

    if request.method=="POST" :
        couponId =str(uuid.uuid1())
        spendMoney =request.form.get("spendMoney")
        disCount = request.form.get("disCount")
        endTime =request.form.get("endTime")
        title =request.form.get("title")
        if not all([spendMoney,disCount,endTime,title]):
            responseData["status"]=1 
            responseData["message"]="缺少必要的业务参数!"
        else:
            coupon= Coupon(couponId=couponId,spendMoney=spendMoney,disCount=disCount,endTime=endTime,title=title)
            db.session.add(coupon)
            db.session.commit()
            responseData["status"]=0 
            responseData["message"]="添加成功!"

    return jsonify(responseData)



#查询系统所有的优惠券
@app.route('/systemCoupon',methods=["POST"])
def systemCoupon():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}
    }
    couponList = Coupon.query.filter().all()
    responseData["message"]="获取系统优惠券成功!"
    return jsonify(responseData)


#用户领取优惠券
@app.route('/drawCoupon',methods=["POST"])
def drawCoupon():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{}
    }
    userId='111'
    couponId =request.form.get("couponId")
    if not couponId:
       responseData["status"]=0
       responseData["message"]="缺少必要的业务参数!"
    else:
        usercoupon=UserCoupon(userId=userId,couponId=couponId)
        db.session.add(usercoupon)
        db.session.commit()
        responseData["status"]=0 
        responseData["message"]="优惠券领取成功!"
    return jsonify(responseData)



#获取用户优惠券
@app.route('/userCoupon',methods=["POST"])
def userCoupon():
    #返回参数结构
    responseData={
        "status":0,
        "message":'',
        "result":{
            "couponList":[]
        }
    }
    userId='111'
    couponList= UserCoupon.query.filter(userId==userId).all()
    responseData["status"]=0 
    responseData["message"]="优惠券领取成功!"
    # responseData["result"]["couponList"]=couponList
    return jsonify(responseData)



#用户收藏商品
@app.route('/collect',methods=["post"])
def collect():
    #返回参数结构
    responseData={
        "status":0,
        "message":"",
        "result":{}
    }
    goodsId=request.form.get("goodsId")
    userId="111"
    collectId =str(uuid.uuid1())
    if not goodsId :
        responseData["status"]=1
        responseData["message"]="缺少必要的业务参数"
    else:
        goods=Collect(goodsId=goodsId,userId=userId,collectId=collectId)
        db.session.add(goods)
        db.session.commit()
        responseData["status"]=0 
        responseData["message"]="收藏商品成功!"
    return jsonify(responseData)


#查询用户收藏商品
@app.route('/userCollect',methods=["post"])
def userCollect():
    #返回参数结构
    responseData={
        "status":0,
        "message":"",
        "result":{
            "collectList":[]
        }
    }
    userId="1"
    collectList=Collect.query.filter(Collect.userId==userId).all()
    print collectList
    return collectList


#从收藏列表中删除
@app.route('/delCollect',methods=["POST"])
def delCollect():
    #返回参数结构
    responseData={
        "status":0,
        "message":"",
        "result":{}
    }
    collectId=request.form.get("collectId")
    userId='111'
    if not collectId:
        responseData["status"]=1
        responseData["message"]="缺少必要的业务参数"
    else:
        goods=Collect.query.filter(and_(Collect.userId==userId,Collect.collectId==collectId)).first()
        if not goods:
           responseData["status"]=1 
           responseData["message"]="操作失败,请稍后重试!"   
        else:
            db.session.delete(goods)
            db.session.commit()
            responseData["status"]=0 
            responseData["message"]="已成功从收藏列表中移除!"
    return jsonify(responseData)


@app.route('/searchGoods',methods=["POST"])
def searchGoods():
    #返回参数结构
    responseData={
        "status":0,
        "message":"",
        "result":{}
    }

    keyword=request.form.get("keyword")
    if not keyword:
        responseData["status"]=1
        responseData["message"]="请输入搜索关键词"
    else:
        goods=Goods.query.filter(Goods.goodsName.like('%user%')).first()
        print goods

    return 'a'    
                    
                     
        

    


    
                      
            
                
            
                   
        

    


            
          

    
             

    
        
                
                
                

                         
                
                   
            
            



if __name__ == '__main__':
      app.run(debug=True,host='192.168.100.52')