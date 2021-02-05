
from app import ma,db
from .models import User
from marshmallow import validates,ValidationError
class UserSchema(ma.Schema):
    class Meta:
        sqla_session=db.session

        model=User
        fields=['id','username','email','password_hash']

    @validates('username')
    def redundant_username(self,value):
            user = User.query.filter_by(username=value).first()
            if user is not None:
                raise ValidationError("Username already exists")

    @validates('email')
    def redundant_email(self,value):
        user = User.query.filter_by(username=value).first()
        if user is not None:
            raise ValidationError("Email already exists")



user_schema=UserSchema(unknown='EXCLUDE')
users_schema=UserSchema(many=True)

