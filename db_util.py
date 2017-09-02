import os
import logging

import pymysql

class DbManagerException(Exception):
    pass

class DbManager(object):
    DB_CREATE = 'CREATE DATABASE %s'
    DB_DROP = 'DROP DATABASE IF EXISTS %s'
    DB_USE = 'USE %s'
    DB_CREATE_TABLE = 'CREATE TABLE %s (%s) DEFAULT CHARSET=utf8'
    DB_INSERT = 'INSERT INTO %s (%s) VALUES'
    DB_SELECT = 'SELECT %s FROM '

    def __init__(self, host, user, password, loglvl=logging.INFO):
        self.conn = None
        self.cursor = None
        self._setuplogging(loglvl)
        self._init_conn(host, user, password)
        self._init_cursor()

    def _setuplogging(self, loglvl):
        self.logger = logging.getLogger(self.__class__.__name__)
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(loglvl)
        self.logger.addHandler(ch)
        self.logger.setLevel(loglvl)

    def _init_conn(self, host, user, password):
        self.logger.info('Connecting to MySQL database')
        self.conn = pymysql.connect(host=host, user=user,
                                    password=password,
                                    charset='utf8mb4')

    def _init_cursor(self):
        self.logger.info('Creating cursor instance')
        self.cursor = self.conn.cursor()

    def commit(self):
        self.logger.info('Commit changes')
        try:
            self.conn.commit()
        except AttributeError, e:
            raise DbManagerException('Connection to database is closed', str(e))
        except pymysql.err.InterfaceError, e:
            raise DbManagerException('Connection to database is closed', str(e))

    def create_db(self, dbname):
        self.logger.info('Creating db: %s', dbname)
        try:
            self.cursor.execute(DbManager.DB_CREATE %(dbname))
        except pymysql.err.ProgrammingError, e:
            raise DbManagerException('Error creating %s database' % dbname, str(e))
        except pymysql.err.InterfaceError, e:
            raise DbManagerException('Connection to database is closed', str(e))

    def delete_db(self, dbname):
        self.logger.info('Deleting db: %s', dbname)
        try:
            self.cursor.execute(DbManager.DB_DROP %(dbname))
        except pymysql.err.InterfaceError, e:
            raise DbManagerException('Connection to database is closed', str(e))

    def recreate_db(self, dbname):
        self.delete_db(dbname)
        self.create_db(dbname)

    def close(self):
        self.logger.info('Closing connection to MySQL database')
        try:
            self.conn.close()
        except AttributeError, e:
            raise DbManagerException('Connection already closed.', str(e))
        self.conn = None

    def use_db(self, dbname):
        self.logger.info('Current db: %s', dbname)
        try:
            self.cursor.execute(DbManager.DB_USE %(dbname))
        except pymysql.err.InterfaceError, e:
            raise DbManagerException('Connection to database is closed', str(e))

    def create_table(self, table_name, column_info):
        self.logger.info('Creating table: %s', table_name )
        try:
            self.cursor.execute(DbManager.DB_CREATE_TABLE % (table_name, column_info))
        except pymysql.err.InternalError, e:
            raise DbManagerException('Error creating %s table' % table_name, str(e))
        except pymysql.err.InterfaceError, e:
            raise DbManagerException('Connection to database is closed', str(e))

    def insert_table_data(self, table_name, cols, vals):
        self.logger.info('Inserting values into %s', table_name)
        cols = ', '.join(['`'+i+'`' for i in cols])
        sql_str = DbManager.DB_INSERT % (table_name, cols) +\
                            '('+ '%s, '*(len(vals) - 1)+'%s)'
        try:
            self.cursor.execute(sql_str, tuple(vals))
        except pymysql.err.IntegrityError, e:
            raise DbManagerException('Duplicate entry ', str(e))
        except pymysql.err.InterfaceError, e:
            raise DbManagerException('Connection to database is closed', str(e))
        self.commit()

    def select_table_data(self, table_name, cols):
        self.logger.info('Select values from %s', table_name)
        cols = ', '.join(['`'+i+'`' for i in cols])
        sql_str = (DbManager.DB_SELECT + table_name) % (cols)
        try:
            self.cursor.execute(sql_str)
            return self.cursor.fetchall()
        except pymysql.err.InterfaceError, e:
            raise DbManagerException('Connection to database is closed', str(e))

