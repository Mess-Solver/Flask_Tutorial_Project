from .serializers import user_schema, users_schema
from app import db
from.models import User
from flask import request,jsonify
from . import app
from marshmallow import ValidationError,validates

#create user
@app.route('/api/create',methods=['GET','POST'])
def create_user():
    #username=request.json['username']
    #email=request.json['email']
    password=request.json['password']
    try:
        deserialized_data=user_schema.load(request.json)
    except ValidationError as err:
        raise err
    user=User(username=deserialized_data["username"],email=deserialized_data["email"])
    user.create_password(password)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)


#read all
@app.route('/api',methods=['GET','POST'])
def get_all_user():
    users=User.query.all()
    result=users_schema.dump(users)
    return jsonify(result)

@app.route('/api/<id>',methods=['GET','POST'])
def get_user(id):
    user=User.query.get(id)

    return user_schema.jsonify(user)





