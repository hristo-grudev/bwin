# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from itemadapter import ItemAdapter


class BwinPipeline:
    conn = sqlite3.connect('bwin.db')
    cursor = conn.cursor()

    def open_spider(self, spider):
        self.cursor.execute(r'CREATE TABLE IF NOT EXISTS `bwin` (id INTEGER PRIMARY KEY AUTOINCREMENT, site varchar(100), sport text, date date, participant1 text, participant2 text, coeff1 REAL, coeffX REAL, coeff2 REAL)')
        self.conn.commit()

    def process_item(self, item, spider):
        site = item['site']
        sport = item['sport']
        date = item['date']
        participant1 = item['participant1']
        participant2 = item['participant2']
        coeff1 = item['coeff1']
        coeffX = item['coeffX']
        coeff2 = item['coeff2']


        self.cursor.execute(f'select * from bwin where site = "{site}" and date = "{date}" and date = "{participant1}" and date = "{participant2}"')
        is_exist = self.cursor.fetchall()

        # print(f'insert into `bwin` (rowid, `site`, `sport`, `date`, `participant1`, `participant2`, `coeff1`, `coeffX`, `coeff2`) values ("{site}", "{sport}", "{date}", "{participant1}", "{participant2}", "{coeff1}", "{coeffX}", "{coeff2}")')

        if len(is_exist) == 0:
            self.cursor.execute(
                f'insert into `bwin` (`site`, `sport`, `date`, `participant1`, `participant2`, `coeff1`, `coeffX`, `coeff2`) values ("{site}", "{sport}", "{date}", "{participant1}", "{participant2}", "{coeff1}", "{coeffX}", "{coeff2}")'
            )
            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()