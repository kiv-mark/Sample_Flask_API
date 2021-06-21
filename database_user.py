from connection import Database_Work
from passlib.hash import sha256_crypt
from logger import Logger
from sqlite3 import Error


class Users(object):

    def __init__(self):
        self.obj_db = Database_Work()
        self.logger = Logger()

    def get_users(self):
        pass

    def insert_user(self, username, password, role):

        try:
            password = sha256_crypt.encrypt(password)
            sql_insert_user = "INSERT INTO USERS VALUES ('" + username + "','" + password + "', {});".format(role)
            c = self.obj_db.conn.cursor()
            c.execute(sql_insert_user)
            self.logger.debug("Users Table created successfully !!")
            self.obj_db.conn.commit()
            return True

        except Error as e:
            self.logger.error(e)
            return False

    def update_user(self, username, password, role):

        try:
            password = sha256_crypt.encrypt(password)
            # UPDATE Students SET DepartmentId = 3 WHERE StudentId = 6;
            sql_update_user = "UPDATE USERS SET password ='"+password+"' WHERE user_name = '"+username+"';"
            c = self.obj_db.conn.cursor()
            c.execute(sql_update_user)
            self.logger.debug("Users Table updated successfully !!")
            self.obj_db.conn.commit()
            return True

        except Error as e:
            self.logger.error(e)
            return False

    def delete_user(self, username):

        try:
            sql_delete_user = "DELETE FROM USERS WHERE user_name = '"+username+"';";
            c = self.obj_db.conn.cursor()
            c.execute(sql_delete_user)
            self.logger.debug("Users Table updated successfully !!")
            self.obj_db.conn.commit()
            return True

        except Error as e:
            self.logger.error(e)
            return False
