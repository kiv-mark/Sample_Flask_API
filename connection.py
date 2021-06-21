import sqlite3
from sqlite3 import Error
from logger import Logger
from passlib.hash import sha256_crypt


class Database_Work(object):

    def __init__(self):
        self.conn = None
        self.db_file = "Project_db.db"
        self.conn = sqlite3.connect(self.db_file)
        self.logger = Logger()

    def create_user_table(self):
        """ create a table from the sql_create_users_table statement
        :return True or False:
        """
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                            user_name text PRIMARY KEY,
                                            password text NOT NULL
                                        ); """
        try:
            c = self.conn.cursor()
            c.execute(sql_create_users_table)
            self.logger.debug("Users Table created successfully !!")
            return True
        except Error as e:
            self.logger.error(e)
            return False

    def check_user_table(self):
        """ checking table exists or not
        :return True or False:
        """
        table_name = "users "
        try:
            query = "SELECT name from sqlite_master WHERE type='table' AND name='" + table_name + "';"
            cursor = self.conn.execute(query)
            result = cursor.fetchone()
            if result:
                self.logger.debug("User Table Exists")
                return True
            else:
                self.logger.info("User Table Doesn't Exists")
                return False

        except Error as e:
            self.logger.error(e)
            return False

    def insert_default_user(self):
        """ inserting default admin user
        :return True or False:
        """
        username = "admin"
        passwd = "HP1nvent"
        password = sha256_crypt.encrypt(passwd)
        role = 1

        try:
            insert_query = "INSERT INTO USERS VALUES ('"+username+"','"+password+"', {});".format(role)
            self.logger.debug(insert_query)
            c = self.conn.cursor()
            c.execute(insert_query)
            self.logger.info("Added admin user successfully !!")
            self.conn.commit()
            return True
        except Error as e:
            self.logger.error(e)
            return False

    def login(self, username):
        """ checking user for login
        :return True or False:
        """

        try:
            select_query = "SELECT USER_NAME, PASSWORD FROM USERS WHERE USER_NAME='"+username+"';"
            self.logger.debug(select_query)
            cursor = self.conn.execute(select_query)
            rows = cursor.fetchall()
            self.logger.debug(rows)
            if rows:
                self.logger.debug(username+" user found !!")
                self.logger.debug(rows)
                return rows[0][0], rows[0][1]
            else:
                self.logger.debug(username+" user not found !!")
                return False
        except Error as e:
            self.logger.error(e)
            return False

    def get_role(self, username):
        """ checking user role for authorization
        :return True or False:
        """

        try:
            select_query = "SELECT ROLE FROM USERS WHERE USER_NAME='" + username + "';"
            self.logger.debug(select_query)
            cursor = self.conn.execute(select_query)
            rows = cursor.fetchall()
            self.logger.debug(rows)
            if rows:
                self.logger.debug(username + " user's role found !!")
                return rows[0][0]
        except Error as e:
            self.logger.error(e)
            return False


if __name__ == '__main__':
    obj = Database_Work()
    val = obj.check_user_table()
    if not val:
        obj.create_user_table()
        obj.insert_default_user()

