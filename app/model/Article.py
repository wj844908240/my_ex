# -*- coding: utf-8 -*-
from elasticsearch_dsl import DocType, Nested, Date, Boolean, analyzer,Completion, Keyword,Text, Integer
from datetime import datetime
from config import connections


class Article(DocType):
    title = Text()
    published = Boolean()
    author = Text()
    content = Text()
    add_ip = Text()
    category = Text()
    point_num = Integer()
    commont_num = Integer()
    fav_num = Integer()

    class Meta:
        # 数据库名称和表名称
        index = "zzh"
        doc_type = "article"

    def save(self, **kwargs):
        self.addtime = datetime.now()
        return super(Article, self).save(**kwargs)

if __name__ == '__main__':
    Article.init()