#!/usr/bin/env python

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from index import app
from models import db, User,Address,Goods,Cart,Order,Collect,Coupon,UserCoupon,Chosen,Discount
manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()
