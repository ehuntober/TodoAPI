from dataclasses import field
from email.policy import default
from unicodedata import name
from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


# instantiate flask app
app = Flask(__name__)

# set configs
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# instantiate db object
db = SQLAlchemy(app)

# create Marshmallow object
ma = Marshmallow(app)

# create database
class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    completed = db.Column(db.Boolean, nullable=False,default=False)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.id

# create Todolist Schema

class TodolistSchema(ma.Schema):
    class Meta:
        fields= ('name','description','completed','date_completed')

# create instance of schema
todolist_schema = TodolistSchema(many=False)
todolist_schema = TodolistSchema(many=True)

# create todos route
@app.route('/todolist', methods=['POST'])
def add_todo():

    try:
        name = request.json['name']
        description = request.json['description']

        new_todo = TodoList(name=name, description =description)

        db.session.add(new_todo)
        db.session.commit()

        return todolist_schema.jsonify(new_todo)
    except Exception as e:
        return jsonify({'Error': 'Invalid request'})


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)