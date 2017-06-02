from passlib.apps import custom_app_context as pwd_context
import datetime, jwt

from run import db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)



class BucketList(db.Model):

    __tablename__ = 'bucket_list'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    items = db.Column(db.String(50), nullable = True)
    date_created = db.Column(db.Date, nullable = False)
    date_modified = db.Column(db.Date, nullable = False)
    created_by = db.Column(db.Date)
    done = db.Column(db.Boolean, default=False) 
    items = db.relationship('Item', backref='bucket_list',
                            cascade='all, delete', lazy='dynamic')
        
class Item(db.Model):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.Date(), nullable = False)
    date_modified = db.Column(db.Date(), nullable = False)
    list_id = db.Column(db.Integer, db.ForeignKey('bucket_list.id'))
    done = db.Column(db.Boolean, default=False)
 