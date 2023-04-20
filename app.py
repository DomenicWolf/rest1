"""Flask app for Cupcakes"""

from models import db, connect_db,Cupcake
from flask import Flask,request,render_template,redirect,flash,session,jsonify
from flask_debugtoolbar import DebugToolbarExtension

#from forms import AddSnackForm,NewEmployeeForm
#from map import key,requests
app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///desserts_db'
app.config['SECRET_KEY'] = 'asdasd'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_one_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes',methods=['POST'])
def create_cupcake():
    new_cupcake = Cupcake(flavor=request.json['flavor'],size=request.json['size'],rating=request.json['rating'],image=request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    json_response = jsonify(cupcake = new_cupcake.serialize())
    return (json_response,201)

@app.route('/api/cupcakes/<int:cupcake_id>',methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='deleted')