# -*- coding: utf-8 -*-
import pyodbc


class Connection:
    def __init__(self, ip, database, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.database = database
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 11 for SQL Server}'
                + ';SERVER=' + self.ip
                + ';DATABASE=' + self.database
                + ';UID=' + self.username
                + ';PWD=' + self.password
                , autocommit=False)
            self.cursor = self.conn.cursor()
        except Exception as err:
            raise err

    def batch_parameterized_insert(self, sql, records):
        try:
            self.cursor.executemany(sql, records)
        except pyodbc.DatabaseError as err:
            self.conn.rollback()
            raise err
        else:
            self.conn.commit()
        finally:
            self.cursor.fast_executemany = False

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except pyodbc.DatabaseError as err:
            self.conn.rollback()
            raise err
        else:
            self.conn.commit()

    def parameterized_execute(self, sql, parameters=None):
        try:
            self.cursor.execute(sql, parameters)
        except pyodbc.DatabaseError as err:
            self.conn.rollback()
            raise err
        else:
            self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
