from flask import Flask, request, make_response, jsonify
from flask_restx import Resource, Namespace
from database.database import Database

user = Namespace('user')

@user.route('')
class UserManagement(Resource):
    def get(self):
        # GET method 구현 부분
        db =Database()

        id = request.args.get('id')
        pw = request.args.get('password')

        quary = "select * from JaeHyukDATABASE.user where id = %s;"
        row = db.execute_one(quary,(id))

        if row is None:
            response = jsonify({"is_success":False ,"message" : "해당 유저가 존재하지 않음"})
            return make_response(response,400)

        quary = "select * from JaeHyukDATABASE.user where id = %s and pw = %s;"
        row = db.execute_one(quary,(id,pw))

        if row is None:
            response = jsonify({"is_success":False ,"message" : "아이디나 비밀번호 불일치"})
            return make_response(response,400)

        response = jsonify({"nickname" : "%s"%(row['nickname'])})
        return make_response(response,200)

    def post(self):
        # POST method 구현 부분
        db =Database()
        userData = request.get_json()

        quary = "select * from JaeHyukDATABASE.user where id = %s;"
        row = db.execute_one(quary,(userData['id']))

        if row is not None:
            response = jsonify({"is_success":False ,"message" : "이미 있는 유저"})
            return make_response(response,400)
             
        quary = "insert into JaeHyukDATABASE.user values(%s,%s,%s);"
        db.execute(quary,(userData['id'],userData['password'],userData['nickname']))
        db.commit()

        response = jsonify({"is_success":True ,"message" : "유저 생성 성공"})
        return make_response(response,200)


    def put(self):
        # PUT method 구현 부분
        db =Database()
        userData = request.get_json()

        quary = "select * from JaeHyukDATABASE.user where id = %s and pw = %s;"
        row = db.execute_one(quary,(userData['id'],userData['password']))

        if row is None:
            response = jsonify({"is_success":False ,"message" : "아이디나 비밀번호 불일치"})
            return make_response(response,400)

        #return row['nickname'] +" and "+ userData['nickname']
        if row['nickname'] == userData['nickname']:
            response = jsonify({"is_success":False ,"message" : "현재 닉네임과 같음"})
            return make_response(response,400)

        quary = "update JaeHyukDATABASE.user set nickname = %s where nickname = %s;"
        db.execute(quary,(userData['nickname'],row['nickname']))
        db.commit()

        response = jsonify({"is_success":True ,"message" : "유저 닉네임 변경 성공"})
        return make_response(response,200)
    

    def delete(self):
        # DELETE method 구현 부분
        db = Database()
        userData = request.get_json()

        quary = "select * from JaeHyukDATABASE.user where id = %s and pw = %s;"
        row = db.execute_one(quary,(userData['id'],userData['password']))

        if row is None:
            response = jsonify({"is_success":False ,"message" : "아이디나 비밀번호 불일치"})
            return make_response(response,400)

        quary = "Delete from JaeHyukDATABASE.user where id = %s;"
        db.execute(quary,(userData['id']))
        db.commit()

        response = jsonify({"is_success":True ,"message" : "유저 삭제 성공"})
        return make_response(response,200)