from flask import Flask, request, make_response, jsonify
from flask_restx import Resource, Namespace
from database.database import Database

user = Namespace('user')

@user.route('')
class UserManagement(Resource):
    def get(self):
        # GET method 구현 부분
        userData = request.get_json()

        quary = "select * from JaeHyukDATABase.user where id = %s;"
        row = Database.execute_one(self,quary,(userData['id']))

        if row['id'] is None:
            response = jsonify({"is_success":False ,"message" : "아이디어나 비밀번호 불일치"})
            return make_response(response,400)

        quary = "select * from JaeHyukDATABase.user where id = %s and pw = %s;"
        row = Database.execute_one(self,quary,(userData['id'],userData['pw']))

        if row['id'] is None:
            response = jsonify({"is_success":False ,"message" : "아이디어나 비밀번호 불일치"})
            return make_response(response,400)

        response = jsonify({"is_success":True ,"nickname" : "%s"%(row['nickname'])})
        return make_response(response,200)

    def post(self):
        # POST method 구현 부분
        userData = request.get_json()

        quary = "select * from JaeHyukDATABase.user where id = %s;"
        row = Database.execute_one(self,quary,(userData['id']))

        if row['id'] is not None:
            response = jsonify({"is_success":False ,"message" : "이미 있는 유저"})
            return make_response(response,400)
             
        quary = "insert into JaeHyukDATABase.user values(%s,%s,%s);"
        Database.execute(self,quary,(userData['id'],userData['passward'],userData['nickname']))
        Database.commit(self)

        response = jsonify({"is_success":True ,"message" : "유저 생성 성공"})
        return make_response(response,200)


    def put(self):
        # PUT method 구현 부분
        userData = request.get_json()

        quary = "select * from JaeHyukDATABase.user where id = %s and pw = %s;"
        row = Database.execute_one(self,quary,(userData['id'],userData['pw']))

        if row['id'] is None:
            response = jsonify({"is_success":False ,"message" : "아이디어나 비밀번호 불일치"})
            return make_response(response,400)

        if row['nickname'] is userData['nickname']:
            response = jsonify({"is_success":False ,"message" : "현재 닉네임과 같음"})
            return make_response(response,400)

        quary = "Set SQL_SAFE_UPDATES = 0;"
        Database.execute(self,quary)
        Database.commit(self)

        quary = "update JaeHyukDATABase.user set nickname = %s where nickname = %s;"
        Database.execute(self,quary,(userData['nickname'],row['nickname']))
        Database.commit(self)

        response = jsonify({"is_success":True ,"message" : "유저 닉네임 변경 성공"})
        return make_response(response,200)
    

    def delete(self):
        # DELETE method 구현 부분
        userData = request.get_json()

        quary = "select * from JaeHyukDATABase.user where id = %s and pw = %s;"
        row = Database.execute_one(self,quary,(userData['id'],userData['pw']))

        if row['id'] is None:
            response = jsonify({"is_success":False ,"message" : "아이디어나 비밀번호 불일치"})
            return make_response(response,400)

        quary = "Delete from JaeHyukDATABase.user where id = %s;"
        Database.execute(self,quary,(userData['id']))
        Database.commit(self)

        response = jsonify({"is_success":True ,"message" : "유저 삭제 성공"})
        return make_response(response,200)