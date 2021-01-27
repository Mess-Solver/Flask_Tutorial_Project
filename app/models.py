from app import db


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,index=True)
    email=db.Column(db.String(50),unique=True, index=True)
    password_hash=db.Column(db.String(100))

    def __repr__(self):
        return "User : {}".format(self.username)

