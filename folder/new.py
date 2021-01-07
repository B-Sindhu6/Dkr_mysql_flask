from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import time

time.sleep(300)
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://username:secretpassword@host:3306/mydb1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(150), unique=True)
    country = db.Column(db.String(25))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    
    def __init__(self, name, address, country, lat, lng):
        self.name = name
        self.address = address
        self.country = country
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return '<data %r>' % self.name

db.create_all()

@app.route('/')
def home():
    b = []
    a = db.session.execute('Select country from `data`').fetchall()
    [b.append(i[0]) for i in a if i[0] not in b]
    return render_template('home.html', countries=b)


@app.route('/univ/', methods=['POST', 'GET'])
def university():
    if request.method == 'POST':
        name = request.form.get('university')
    else:
        name = request.args.get('university')
    a = db.session.execute('Select * from `data` where name like "%s"'%name)
    row = a.fetchone()
    if row is None:
        return render_template('result.html')
    else:
        keys = ['id','name', 'address', 'lat', 'lon', 'country']
        dic = dict(zip(keys, row))
        return render_template('result.html', values=dic)


@app.route('/country/', methods=['POST'])
def country():
    cname = request.form.get('country')
    r = []
    cur = db.session.execute('select name,address from `data` where country like "%s"'%cname)
    r = [row[0] for row in cur]
    if len(r) < 1:
        return render_template('result.html')
    return render_template('result.html', c=1, values=r)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
