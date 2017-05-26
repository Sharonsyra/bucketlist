from run import db

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(20), nullable = False)
    bucketlists = db.relationship('Bucketlist', backref='user',
                                  cascade='all,delete', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hashed_password(password)

    def hashed_password(self, new_password):
        """
        Hashes the new entered password
        """
        self.password = generate_password_hash(new_password)

    
    def generate_token(self, expiration = 1200):
        """
        generates token
        """
        serialize = Serialize(app.config['SECRET_KEY'], expire_time = expiration)
        return serialize.dumps({'id': self.id})

    def __repr__(self):
        return '<User {}>'.format(self.username)



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
 