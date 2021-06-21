from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from logger import Logger
from connection import Database_Work
from database_user import Users
from passlib.hash import sha256_crypt


auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verify(username, password):
    try:
        logger = Logger()
        database = Database_Work()
        user, passwd = database.login(username)
        logger.debug(user, passwd)
        if not (username and password):
            return False
        elif user:
            if sha256_crypt.verify(password, passwd):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False

def authorization_login(username):
    database = Database_Work()
    role = database.get_role(username)
    if not role:
        return False
    elif role == 1:
        return True
    else:
        return False



class AddUser(Resource):

    def __init__(self):
        self.logger = Logger()
        self.obj = Users()

    @auth.login_required
    def get(self):
        pass

    @auth.login_required
    def post(self):
        username = request.authorization.username
        if authorization_login(username):
            self.logger.debug("Adding User !!")
            user_details = request.get_json()
            status = self.obj.insert_user(user_details["username"], user_details["password"], user_details["role"])
            if status:
                return {"message": "Success", "user": request.authorization.username}
            else:
                return {"message": "User couldn't be added !!", "user": request.authorization.username}
        else:
            return {"message": "You dont have the access !!"}

    @auth.login_required
    def delete(self):

        self.logger.debug("Adding User !!")
        user_details = request.get_json()
        status = self.obj.delete_user(user_details["username"])
        if status:
            return {"message": "Success"}
        else:
            return {"message": "User couldn't be deleted !!"}


class EditUser(Resource):

    def __init__(self):
        self.logger = Logger()
        self.obj = Users()

    @auth.login_required
    def get(self):
        pass

    @auth.login_required
    def post(self):

        self.logger.debug("Updating User !!")
        user_details = request.get_json()
        status = self.obj.update_user(user_details["username"], user_details["password"])
        if status:
            return {"message": "Success"}
        else:
            return {"message": "User couldn't be added !!"}


api.add_resource(AddUser, '/user/add/')
api.add_resource(EditUser, '/user/update/')

if __name__ == '__main__':
    app.run(debug=True)
