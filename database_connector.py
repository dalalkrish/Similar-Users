# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:46:38 2018

@author: kdalal
"""

import sqlite3
import pandas as pd


class DatabaseWorker(object):
    def __init__(self, db_name):
        self.db = db_name

    def create_table(self, table_name, column_names):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        q1 = 'DROP TABLE IF EXISTS %s' %(table_name)
        q2 = 'CREATE TABLE ' + table_name + ' ' + '(' + ', '.join(str(x) for x in column_names) + ')'
        cur.execute(q1)
        cur.execute(q2)
        conn.commit()
        conn.close()

    def insert_table(self, table_name, data):
        conn = sqlite3.connect(self.db)
        data.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()

    def query_table(self, table_name):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        q = "SELECT * FROM  " + table_name + ";"
        cur.execute(q)
        # row = cur.fetchall()
        row = pd.read_sql_query(q, conn)
        conn.close()
        return row


# ax = DatabaseWorker("example")
# ax.create_table("calldata", data.columns.values.tolist())
# ax.insert_query("calldata", data)
#
# b = ax.query_table1("calldata", '1-OVP793')
# next(b)
