# A simple cafe ammenity listing website
# Admin user credentials are:
# name: Admin
# email: admin@admin.com
# password: 12345678

from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

CAFE_BOOLEANS = ['YES', 'NO']

app = Flask(__name__)
app.config['SECRET_KEY'] = '2954B691B22F6D5757C68DB8AFA7E'
Bootstrap(app)

# Connect to the cafes database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Added for secure login
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    email = db.Column(db.VARCHAR(100), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(100), nullable=False)
    name = db.Column(db.VARCHAR(100), nullable=False)


class Cafe(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(250), nullable=False, unique=True)
    map_url = db.Column(db.VARCHAR(500), nullable=False)
    img_url = db.Column(db.VARCHAR(500), nullable=False)
    location = db.Column(db.VARCHAR(250), nullable=False)
    has_sockets = db.Column(db.BOOLEAN, nullable=False)
    has_toilet = db.Column(db.BOOLEAN, nullable=False)
    has_wifi = db.Column(db.BOOLEAN, nullable=False)
    can_take_calls = db.Column(db.BOOLEAN, nullable=False)
    seats = db.Column(db.VARCHAR(250))
    coffee_price = db.Column(db.VARCHAR(250))


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Google Maps (URL)',
                          validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Image (URL)',
                          validators=[DataRequired(), URL()])
    location = StringField('Cafe Location (City)', validators=[DataRequired()])
    has_sockets = SelectField('Plugins Available', choices=CAFE_BOOLEANS)
    has_toilet = SelectField('Restrooms Available', choices=CAFE_BOOLEANS)
    has_wifi = SelectField('Wifi Available', choices=CAFE_BOOLEANS)
    can_take_calls = SelectField('Can Take Calls', choices=CAFE_BOOLEANS)
    seats = StringField('Seats Available (i.e. 0-10, etc.)',
                        validators=[DataRequired()])
    coffee_price = StringField('Coffee Price (i.e. $2.75, etc.)',
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# Store user ID for secure session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafe_list=all_cafes)


@app.route('/cafe/<int:cafe_id>')
def show_cafe(cafe_id):
    requested_cafe = db.session.query(Cafe).get(cafe_id)
    return render_template('cafe.html', cafe=requested_cafe)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if form.has_sockets.data == 'YES':
            has_sockets_bool = True
        else:
            has_sockets_bool = False
        if form.has_toilet.data == 'YES':
            has_toilet_bool = True
        else:
            has_toilet_bool = False
        if form.has_wifi.data == 'YES':
            has_wifi_bool = True
        else:
            has_wifi_bool = False
        if form.can_take_calls == 'YES':
            can_take_calls_bool = True
        else:
            can_take_calls_bool = False
        new_cafe = Cafe(name=form.name.data,
                        map_url=form.map_url.data,
                        img_url=form.img_url.data,
                        location=form.location.data,
                        has_sockets=has_sockets_bool,
                        has_toilet=has_toilet_bool,
                        has_wifi=has_wifi_bool,
                        can_take_calls=can_take_calls_bool,
                        seats=form.seats.data,
                        coffee_price=form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                error = 'Password incorrect, please try again.'
        else:
            error = 'That email does not exist, please try again.'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if User.query.filter_by(email=request.form.get('email')).first():
            error = "You've already signed up with that email, log in instead."
        else:
            # Hash the users password before storing in database
            hash_password = generate_password_hash(request.form.get('password'),
                                                   method='pbkdf2:sha256',
                                                   salt_length=8)
            new_user = User(email=request.form.get('email'),
                            password=hash_password,
                            name=request.form.get('name'))
            db.session.add(new_user)
            db.session.commit()
            # Login the new user to work with authentication
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('register.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Create Admin User
# db.create_all()
# admin_password = generate_password_hash(
#     'abcd1234', method='pbkdf2:sha256', salt_length=8)
# admin_user = User(email='admin@admin.com',
#                   password=admin_password,
#                   name='Admin')
# db.session.add(admin_user)
# db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
