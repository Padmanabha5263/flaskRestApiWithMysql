from flask import Flask, request, jsonify, json, make_response
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:padmanabha@localhost:3306/customer'

db = SQLAlchemy(app)

class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.String(120), unique=True, nullable=False)    

    def json(self):
        return {'id': self.id,'name': self.name, 'email': self.email, 'phone': self.phone, 'age': self.age}


# getting specific user details
@app.route('/peoples/<int:id>', methods=['GET'])
def getPeople(id):
  try:
    people = People.query.filter_by(id=id).first()
    if people:
      return make_response(jsonify({'Items': people.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except Exception as e:
    return make_response(jsonify({'message': 'error getting user'}), 500)






@app.route('/peoples/<int:id>', methods=['DELETE'])
def deletePeople(id):
    try:
        user = People.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting user'}), 500)





# updating the specific user details
@app.route('/peoples/<int:id>', methods=['PUT'])
def updatePeople(id):
  try:
    user = People.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.name = data['name']
      user.email = data['email']
      user.age = data['age']
      user.phone = data['phone']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except Exception as e:
    return make_response(jsonify({'message': 'error updating user'}), 500)




# gettings all the records from the table
@app.route('/peoples', methods=['GET'])
def getPeoples():
    try:
        peoples = People.query.all()  
        return make_response(jsonify({"Items":[people.json() for people in peoples]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting users'}), 500)





# creating the user detailes in table
@app.route('/peoples', methods=['POST'])
def createPeople():
  try:
    data = request.get_json()
    new_user = People(name=data['name'], email=data['email'], age=data['age'], phone=data['phone'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'user created'}), 201)
  except Exception as e:
    return make_response(jsonify({'message': 'error creating user'}), 500)
  




if __name__ == "__main__":
    app.run(debug=True)

