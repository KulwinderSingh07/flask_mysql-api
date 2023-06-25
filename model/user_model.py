import mysql.connector
import json
from flask import make_response
import os
class user_model():
    def __init__(self):
        try:
            #connection stablishment code
            self.con=mysql.connector.connect(host="localhost",user="Kulwinder",password="Laddi@2002",database="flask-api")
            self.con.autocommit=True
            self.curr=self.con.cursor(dictionary=True)
            print("Connection Succesfull")
        except:
            print("Some error occures to connect to mysql")
    def user_getall_model(self):
        self.curr.execute("select * from User")
        result=self.curr.fetchall()
        print(result)
        if len(result)>0:
            res=make_response({"payload":result},200)
            res.headers['Access-Control-Allow-Origin']="*"
            return res
        else:
            return make_response({"message":"Data not found"},204)
        
    def user_addone_model(self,data):
        # print(data["email"])
        # self.curr.execute("select * from User")
        self.curr.execute(f"insert into User(name,email,phone,password) values('{data['name']}','{data['email']}','{data['phone']}','{data['password']}')")
        return make_response({"message":"user created succesfully"},201)

    def user_updateone_model(self,data):
        self.curr.execute(f"update User set name='{data['name']}', email='{data['email']}', phone='{data['phone']}', password='{data['password']}', role='{data['role']}' where id={data['id']}")
        print(self.curr.rowcount)
        if self.curr.rowcount>0:
            return make_response({"message":"user updated succesfully"},201)
        else:
            return make_response({"message":"User not updated"},202)
        
    def delete_user_model(self,id):
        self.curr.execute(f"DELETE FROM User WHERE id={id}")
        if self.curr.rowcount>0:
            return make_response({"message":"deleted sussesfully"},200)
        else:
            return make_response({"message":"failed to delete user"},202)
        
    def user_patch_model(self,data,id):
        # print(data)
        # print(id)
        qry="update User set "
        for key in data:
            qry+=f"{key}='{data[key]}',"
        qry=qry[:-1]+f" where id={id}"
        # return qry
        self.curr.execute(qry)
        if self.curr.rowcount>0:
            return make_response({"message":"updated attributes succesfully sussesfully"},200)
        else:
            return make_response({"message":"Failed to update user attributes sussesfully"},202)
        
    def user_pagination_model(self,limit,page):
        limit=int(limit)
        page=int(page)
        start=(page*limit)-limit
        qry=f"select * from User limit {start},{limit}"
        self.curr.execute(qry)
        result=self.curr.fetchall()
        if self.curr.rowcount>0:
            res= make_response({"payload":result,"page_no":page,"limit":limit},200)
            return res
        else:
            return make_response({"message":"No data found"},204)
        


