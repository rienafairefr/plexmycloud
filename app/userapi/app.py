from flask import Flask, render_template
from flask_nav.elements import Navbar, View
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import UserMixin, RoleMixin
from flask_nav import Nav

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
    SECRET_KEY='James Bond',
    SECURITY_REGISTERABLE=True,
)

db = SQLAlchemy(app)

nav = Nav(app)
bootstrap = Bootstrap(app)
mail = Mail(app)
roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(),
                                                db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))

@nav.navigation()
def top():
    return Navbar(
        'mysite',
        View('Home', 'index'),
        View('Login', 'login'),
        View('Signup', 'signup'),
    )

@nav.navigation()
def logged():
    return Navbar(
        'mysite',
        View('Home', 'index'),
        View('Logout', 'logout'),
    )



class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
Security(app, user_datastore)


@app.before_first_request
def setupDatabase():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
