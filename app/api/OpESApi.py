# -*- coding: utf-8 -*-
from . import api
from lib.ReturnMessage import returnMsg, returnErrorMsg, returnNoneMsg
from flask import request, json, jsonify, url_for
from UserAuthorityApi import user_require
from flask_jwt_extended import get_jwt_identity
import cec
from model.Article import Article
from config import connections

@api.route('/addArticle', methods=['POST'])
@user_require
def addArticle():
    if not request.json:
        resultDict = returnNoneMsg("failed!")
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    article = Article()

    article.title = dataDict.get('title', None)
    article.author = dataDict.get('author', None)
    article.content = dataDict.get('content', None)
    article.category = dataDict.get('category', None)
    article.point_num = dataDict.get('point_num', None)
    article.commont_num = dataDict.get('commont_num', None)
    article.fav_num = dataDict.get('fav_num', None)
    article.add_ip = request.remote_addr
    article.published = True

    res = article.save()
    if res :
        returnId = {
            'id': article.meta.id,
        }
        resultDict = returnMsg(returnId)
        return jsonify(resultDict)
    else:
        resultDict = returnNoneMsg("add failed!")
        return jsonify(resultDict)
@api.route('/deleteArticle/<string:id>/', methods=['GET'])
@user_require
def deleteArticle(id=None):
    if id is None:
        resultDict = returnNoneMsg("please article id!")
        return jsonify(resultDict)
    article_id = id
    article = Article()
    try :
        article.get(id=article_id).delete()
        resultDict = returnMsg("delete success")
    except Exception, e:
        resultDict = returnNoneMsg("id not exists,delete error")

    return jsonify(resultDict)

@api.route('/updateArticle/', methods=['POST'])
@user_require
def updateArticle():
    if not request.json:
        resultDict = returnNoneMsg("failed!")
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('id', None)
    dataDict.pop("id")
    article = Article()
    try:
        article.get(id=id).update(**dataDict)
        resultDict = returnMsg("update success")
    except Exception, e:
        resultDict = returnNoneMsg("id not exists,update error")
    return jsonify(resultDict)

@api.route('/searchArticle', methods=['POST'])
# @user_require
def searchArticle(k=None):
    if not request.json:
        resultDict = returnNoneMsg("failed!")
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)

    title = dataDict.get('title', None)
    author = dataDict.get('author', None)
    article = Article()
    a = article.search()
    if title :
        a = a.filter('term', published=True).query('match', title=title)

    else :
        a = a.filter('term', published=True).query('match', author=author)
    results = a.execute()
    if results:
        infoList = []
        for messageTable in results:

            dictInfo = {
                "id": messageTable._id,
                "title": messageTable.title,
                "author": messageTable.author,
                "content": messageTable.content,
                "add_ip": messageTable.add_ip,
                "category": messageTable.category,
                "point_num": messageTable.point_num,
                "commont_num": messageTable.commont_num,
                "fav_num": messageTable.fav_num,
            }
            infoList.append(dictInfo)
        resultDict = returnMsg(infoList)
    else:
        resultDict = returnNoneMsg("the message not exit!")
    return jsonify(resultDict)
