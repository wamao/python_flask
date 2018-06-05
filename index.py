
# -- coding: utf-8 --
from flask import Flask
from flask import jsonify
from flask_cors import *
from flask import request
from models import User,db,Address,Cart
import uuid
import config  # 配置文件
import sys
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
        user = User.query.filter(User.username == username,User.password == password).first()
        if user:
           responseData["status"]=0 
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
                    user = User(username=username,password=password)
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
        if not(ContactPerson and ContactNumber and ContactAddress and ContactDetailAddress ) :
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
   
    if not(ContactPerson and ContactNumber and ContactAddress and ContactDetailAddress and AddressId ) :
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
        goods = Cart.query.filter(Cart.userId == userId,Cart.goodsId == goodsId,).first()
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
def category():
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

    


            
          

    
             

    
        
                
                
                

                         
                
                   
            
            



if __name__ == '__main__':
      app.run(debug=True,host='192.168.100.52')