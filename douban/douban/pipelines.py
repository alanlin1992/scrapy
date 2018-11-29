# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class DoubanPipeline(object):

    def __init__(self):
        db_args=dict(
            host="192.168.1.128",#数据库主机ip
            db="test",#数据库名称
            user="root",#用户名
            passwd="nomore532",#密码
            charset='utf8',#数据库字符编码
            cursorclass = MySQLdb.cursors.DictCursor,#以字典的形式返回数据集
            use_unicode = True,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **db_args)

    def process_item(self, item, spider):
    	self.dbpool.runInteraction(self.insert_into_quotes, item)
        return item


    def insert_into_quotes(self,conn,item):

        conn.execute(
            '''
            INSERT INTO douban(serial_num,movie_name,introduce,star,evaluate,movie_describe)
            VALUES(%s,%s,%s,%s,%s,%s)
            '''
            ,(item['serial_num'],item['movie_name'],item['introduce'],item['star'],item['evaluate'],item['movie_describe'])
        )

    # def insert_into_quotes(self,conn,item):
    #     conn.execute(
    #         '''
    #         INSERT INTO douban(serial_num,movie_name,introduce,star,evaluate,describe)
    #         VALUES(%s,%s,%s,%s,%s,%s)
    #         '''
    #         ,(item['serial_num'],item['movie_name'],item['introduce'],item['star'],item['evaluate'],item['describe'])
    #     )
