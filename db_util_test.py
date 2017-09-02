
import os
import unittest

from db_util import DbManager, DbManagerException

DB_NAME = 'tester'
TABLE_NAME = 'test'

class TestDbUtils(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDbUtils, self).__init__(*args, **kwargs)
        self.db = None

    def setUp(self):
        self.db = DbManager(host=os.environ['DB_HOST'], user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])

    def test_commit_close(self):
        print ">>> commit and close"
        self.db.close()
        self.assertRaises(DbManagerException, self.db.close)
        self.assertRaises(DbManagerException, self.db.commit)
        self.setUp()
        print "<<< commit and close"

    def test_createdb(self):
        print ">>> create db : del, create"
        self.db.create_db(DB_NAME)
        self.assertRaises(DbManagerException, self.db.create_db, DB_NAME)
        self.db.delete_db(DB_NAME)
        print "<<< create db"

    def test_createtable(self):
        print ">>> create table : use, create"
        self.db.create_db(DB_NAME)
        self.db.use_db(DB_NAME)
        self.db.create_table(TABLE_NAME,
                ("NAME CHAR(100) NOT NULL UNIQUE," "AGE INT"))
        self.assertRaises(DbManagerException, self.db.create_table, TABLE_NAME,
                ("NAME CHAR(100) NOT NULL UNIQUE," "AGE INT"))
        self.db.delete_db(DB_NAME)
        print "<<< create table"

    def test_inserttable(self):
        print ">>> insert table : use, insert, select"
        self.db.create_db(DB_NAME)
        self.db.use_db(DB_NAME)
        self.db.create_table(TABLE_NAME,
                ("NAME CHAR(100) NOT NULL UNIQUE," "AGE INT"))
        self.db.insert_table_data(TABLE_NAME, ['NAME', 'AGE'],['asd', '14'])
        res = self.db.select_table_data(TABLE_NAME, ['*'])
        self.assertEqual(res, ((u'asd', 14),))
        self.assertRaises(DbManagerException, self.db.insert_table_data, TABLE_NAME, ['NAME', 'AGE'],['asd', '14'])
        self.db.delete_db(DB_NAME)
        print "<<< insert table"

    def tearDown(self):
        self.db.close()
        self.db = None

if __name__ == '__main__':
    unittest.main()
