# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False, index=True)
    email = Column(String(80), unique=True, nullable=True, index=True)
    password_hash = Column(String(64))
    categories = relationship('Category', backref='user', lazy=True)

    #def __init__(self, id, username, email, password_hash, categories):

    def __repr__(self):
        return "<User(username='%s')>" % (self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=False, nullable=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    links = relationship('Link', backref='category', lazy=True)

    def __repr__(self):
        return "<Category(id='%s', title='%s', user_id='%s')>" % (self.id, self.content, self.user_id)

class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=False, nullable=True, index=True)
    url = Column(String(360), unique=False, nullable=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return "<Link(id='%s', title='%s', url='%s', category_id='%s')>" % (self.id, self.title, self.url, self.category_id)
