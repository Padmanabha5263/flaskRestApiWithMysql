from flask import Flask, request, jsonify,  make_response
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.getenv("mysqlUsername")+':'+os.getenv("mysqlPassword")+'@pndatabase.cmlgt0igecja.ap-south-1.rds.amazonaws.com:3306/'+os.getenv("mysqlDatabase")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api=Api(app)
db = SQLAlchemy(app)

class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120),unique=True)
    phone = db.Column(db.String(120))
    age = db.Column(db.String(120))
    # created_at = db.Column(db.DateTime(120))  

    def json(self):
        return {'id': self.id,'name': self.name, 'email': self.email, 'phone': self.phone, 'age': self.age}

parser = reqparse.RequestParser()
parser.add_argument("id", type=str)
parser.add_argument("name",type=str)
parser.add_argument("email", type=str)
parser.add_argument("phone", type=str)
parser.add_argument("age", type=int)


class PeopleRoutes(Resource):
    def get(self,id=None):
        try:
            if id==None:
                peoples = People.query.all()  
                return make_response(jsonify({"Items":[people.json() for people in peoples]}), 200)
            
            peoples= People.query.filter_by(id=id).first()
            return {"Items":peoples.json()}, 200
        except Exception as e:
            return make_response(jsonify({'message': 'error getting user detailes'}), 500)
        
    def post(self):
        try:
            args= parser.parse_args()
            response = People(id=str(args["name"]+args["phone"]),name=args['name'], email=args['email'], age=args['age'], phone=args['phone'])
            db.session.add(response)
            db.session.commit()
            return make_response(jsonify({"Items":response.json()}), 201)
        except Exception as e:
            return make_response(jsonify({'message': 'error creating user'}), 500)
        
    def put(self,id=None):
        if id!=None:
            try:
                args=parser.parse_args()
                user = People.query.filter_by(id=id).first()
                if user:
                    user.name = args['name']
                    user.email = args['email']
                    user.age = args['age']
                    user.phone = args['phone']
                    db.session.commit()
                    return make_response(jsonify({"Items":user.json()}), 200)
                return make_response(jsonify({'message': 'user not found'}), 404)
            except Exception as e:
                return make_response(jsonify({'message': 'error updating user'}), 500)
        return make_response(jsonify({'message': 'Enter proper user id'}), 500)
    
    def delete(self,id=None):
        if id!=None:
            try:
                user = People.query.filter_by(id=id).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    return make_response(jsonify({'message': 'user deleted'}), 200)
                return make_response(jsonify({'message': 'user not found'}), 404)
            except Exception as e:
                return make_response(jsonify({'message': 'error deleting user'}), 500)
        return make_response(jsonify({'message': 'Enter proper user id'}), 500)
    

api.add_resource(PeopleRoutes, "/peoples/<id>", "/peoples")

if __name__ == "__main__":
    app.run(debug=True)