from flask import Flask, render_template
from flask_login import current_user
from flask_nav.elements import Navbar, View
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import UserMixin, RoleMixin
from flask_nav import Nav
from sqlalchemy import Integer, Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import backref, relationship

from plex_lib import plex
from plex_lib.plex_signin import plex_signin

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
    SECRET_KEY='James Bond',
    SECURITY_REGISTERABLE=True,
    SECURITY_PASSWORD_SALT='salt',
    SECURITY_POST_REGISTER_VIEW='sign_in'
)

db = SQLAlchemy(app)

nav = Nav(app)
bootstrap = Bootstrap(app)
mail = Mail(app)
roles_users = db.Table('roles_users', Column('user_id', Integer(),
                                                ForeignKey('user.id')),
                       Column('role_id', Integer(),
                                 ForeignKey('role.id')))

@nav.navigation()
def top():
    return Navbar(
        'mysite',
        View('Home', 'index'),
        View('Login', 'security.login'),
        View('Signup', 'security.register'),
    )

@nav.navigation()
def logged():
    return Navbar(
        'mysite',
        View('Home', 'index'),
        View('Plex Sign In', 'sign_in'),
        View('Logout', 'security.logout'),
    )



class Role(db.Model, RoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary=roles_users,
                            backref=backref('users', lazy='dynamic'))

    token_id = Column(ForeignKey('token_cache.id'))
    token = relationship('TokenCache', foreign_keys=[token_id])
    
    
class TokenCache(db.Model):
    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey('user.id'))
    user = relationship('User', foreign_keys=[user_id])

    signed_in = Column(Boolean)
    user_cache = Column(String)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def setupDatabase():
    db.create_all()
    session = db.session
    user = User()
    user.email='test@test.com'
    user.password='test'
    user.active = True
    session.add(user)
    session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign_in')
def sign_in():
    if not current_user.token or not current_user.token.signed_in:
        pass
    signin = plex_signin()
    plex_network = plex.Plex(load=False)
    signin.set_authentication_target(plex_network)
    data = signin.plex_network.get_signin_pin()
    return render_template('pin_signin.html')


if __name__ == '__main__':
    app.run()
