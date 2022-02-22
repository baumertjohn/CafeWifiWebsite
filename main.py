from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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


@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafe_list=all_cafes)


@app.route('/cafe/<int:cafe_id>')
def show_cafe(cafe_id):
    requested_cafe = db.session.query(Cafe).get(cafe_id)
    return render_template('cafe.html', cafe=requested_cafe)


# all_cafes = db.session.query(Cafe).all()
# for cafe in all_cafes:
#     print(cafe.has_sockets)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
