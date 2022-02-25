from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL

CAFE_BOOLEANS = ['YES', 'NO']

app = Flask(__name__)
app.config['SECRET_KEY'] = '2954B691B22F6D5757C68DB8AFA7E'
Bootstrap(app)

# Connect to the cafes database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
        new_cafe = Cafe(name = form.name.data,
                        map_url = form.map_url.data,
                        img_url = form.img_url.data,
                        location = form.location.data,
                        has_sockets = has_sockets_bool,
                        has_toilet = has_toilet_bool,
                        has_wifi = has_wifi_bool,
                        can_take_calls = can_take_calls_bool,
                        seats = form.seats.data,
                        coffee_price = form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


# all_cafes = db.session.query(Cafe).all()
# for cafe in all_cafes:
#     print(cafe.has_sockets)
if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
