# -*- coding: utf-8 -*-
from config import jwt
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_raw_jwt
from lib.ReturnMessage import returnNoneMsg
from functools import wraps
from model.User import User
from flask import request
import types


def user_require(fn):
    @jwt_required
    @wraps(fn)
    def _deco():
        # if type(request.json) != types.DictType:
        #     resultDict = returnNoneMsg("failed!")
        #     return jsonify(resultDict)
        userId = get_jwt_identity()
        if not userId:
            resultDict = returnNoneMsg("not find counselorId!")
            return jsonify(resultDict)
        userTable = User.query.filter_by(id=userId).first()
        postJwt = get_raw_jwt()
        postUserToken = postJwt.get("jti")
        if userTable:
            userToken = userTable.user_token
            if userToken == postUserToken:
                return fn()
            else:
                resultDict = returnNoneMsg("the token not mach with sql!")
        else:
            resultDict = returnNoneMsg("this user not exit!")
        return jsonify(resultDict)

    return _deco


@jwt.invalid_token_loader
@jwt.unauthorized_loader
def my_unauthorized_loader(identy):
    dictInfo = "The has no token: %s" % identy
    resultDict = returnNoneMsg(dictInfo)
    return jsonify(resultDict)


@jwt.expired_token_loader
def my_expired_token_callback():
    returnInfo = returnNoneMsg("the token expired!")
    return jsonify(returnInfo)
