# -*- coding: utf-8 -*-
from . import api
from lib.ReturnMessage import returnMsg, returnErrorMsg, returnNoneMsg
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from flask import request, json, jsonify, url_for
from UserAuthorityApi import user_require
from flask_jwt_extended import get_jwt_identity
from  model.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
import time
import cec


# 注册
@api.route('/register', methods=['POST'])
def register():
    if not request.json:
        resultDict = returnNoneMsg("failed!")
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    name = dataDict.get('name', None)
    password = dataDict.get('password', None)
    email = dataDict.get('email', None)
    phone = dataDict.get('phone', None)

    user_info = User.query.filter_by(user_name=name).first()
    if user_info:
        resultDict = returnNoneMsg(cec.code_1)
        return jsonify(resultDict)

    user = User(
        user_name=name,
        email=email,
        phone=phone,
        user_password=generate_password_hash(password),
        user_reg_ip=request.remote_addr
    )
    db.session.add(user)
    db.session.commit()

    resultDict = returnMsg("register success")
    return jsonify(resultDict)


# 登录
@api.route('/login', methods=['POST'])
def login():
    if not request.json:
        resultDict = returnNoneMsg("failed!")
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    name = dataDict.get("name", None)
    password = dataDict.get("password", None)
    if name and password:

        user = User.query.filter_by(user_name=name).first()
        if not user:
            resultDict = returnNoneMsg("user not exists")
            return jsonify(resultDict)
        if not user.check_pwd(password):
            resultDict = returnNoneMsg("Password error")
            return jsonify(resultDict)
    else:
        resultDict = returnNoneMsg("Bad counselorName or counselorPwd")
        return jsonify(resultDict)

    if user:
        user_id = user.id
        userAccessToken = create_access_token(identity=user_id)
        userRefreshToken = create_refresh_token(identity=user_id)
        accessJti = get_jti(userAccessToken)
        refreshJti = get_jti(userRefreshToken)
        user.user_token = accessJti
        user.user_reflesh_token = refreshJti

        db.session.add(user)
        # 提交修改
        db.session.flush()
        db.session.commit()

        dictInfo = {
            "userId": user_id,
            "accessToken": userAccessToken,
            "refreshToken": userRefreshToken,
        }
        resultDict = returnMsg(dictInfo)
    else:
        resultDict = returnNoneMsg("this user not exit")
    return jsonify(resultDict)


@api.route('/getUser', methods=['GET'])
@user_require
def get():
    """
    获取用户信息
    :return: json
    """
    adminId = get_jwt_identity()
    user = User.query.filter_by(id=adminId).first()

    if user :
        returnUser = {
            'id': user.id,
            'username': user.user_name,
            'email': user.email,
            'phone': user.phone,
            'ip_addr' :user.user_reg_ip,
            # 'addtime':user.addtime
        }
        resultDict = returnMsg(returnUser)

    else:
        resultDict = returnNoneMsg("user not exists")
    return jsonify(resultDict)