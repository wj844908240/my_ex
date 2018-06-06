# -*- coding: utf-8 -*-
from sqlalchemy import Column,String,Integer,DateTime
from config import db
from datetime import datetime


class User(db.Model) :
    __tablename__ = "user"

    id = Column(Integer,primary_key=True,nullable=False)
    user_name = Column(String(20),unique=True)
    user_password = Column(String(100))
    email = Column(String(50),unique=True)
    phone = Column(String(11), unique=True)
    addtime = Column(DateTime, nullable=False,default=datetime.now)
    user_reg_ip = Column(String(50))
    user_token = Column(String(100))
    user_reflesh_token = Column(String(100))
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash

        return check_password_hash(self.user_password, pwd)


    def __repr__(self):
        return '<User %r>' % self.user_name
if __name__ == '__main__':
    db.create_all()
