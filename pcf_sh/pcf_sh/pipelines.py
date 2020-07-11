# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem


class MysqlPipeline:

    def __init__(self, mysql_url, mysql_db, mysql_user, mysql_password):
        # self.mysql_url = mysql_url
        # self.mysql_db = mysql_db
        # self.mysql_user = mysql_user
        # self.mysql_password = mysql_password
        self.db = pymysql.connect(host=mysql_url, user=mysql_user, passwd=mysql_password, db=mysql_db)
        self.cursor = self.db.cursor()
        print('successfully connect to database !')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_url=crawler.settings.get('MYSQL_URI'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD')
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # for dict type data
        sql_str = str("insert into " + "pcf_sec" + "(" + ",".join(item.keys()) + ") values(" +
                      "'%s'," * (len(item.keys()) - 1) + "'%s')")
        re_str = ','.join(["item['%s']" % k for k in item.keys()])
        #print(sql_str)
        #print(re_str)
        ex_sql_str = sql_str % eval(re_str)
        # print re_str
        print(ex_sql_str)
        try:
            self.cursor.execute(ex_sql_str)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return item


# 防止重复的数据
class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        key = item['dt'] + item['fund_id'] + item['sec_id'] + item['sec_tag']
        if key in self.ids_seen:
            raise DropItem("Duplicate item found: %r" % item)
        else:
            self.ids_seen.add(key)
            return item


if __name__ == "__main__":
    pass
    print(123)
