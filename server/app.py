from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Import the db object from database.py
from database import db

#import config
import config
#initialize the app
app=Flask(__name__)
#load config
app.config.from_object(config)

#initialize the db with the app
db.init_app(app)

migrate = Migrate(app, db)

#register models
from models import Camper, Activity, Signup

#routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Access Camp"})

#list all campers using GET
@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    campers_list = [{"id": camper.id, "name": camper.name, "age": camper.age} for camper in campers]
    return jsonify(campers_list), 200

#get single camper with signups
@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get(id)
    
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    #construct response with signups
    response = {
        "id": camper.id,
        "name": camper.name,
        "age": camper.age,
        "signups": [{"id": signup.id,"camper_id":signup.camper_id, "activity_id": signup.activity_id, "time": signup.time,
                     'activity': {
                         'id': signup.activity.id,
                         'name': signup.activity.name,
                         'difficulty': signup.activity.difficulty
                                     }
                     } for signup in camper.signups]
    }
    
    return jsonify(response), 200

#create a new camper using POST
@app.route('/campers', methods=['POST'])
def create_camper():
    data = request.get_json()
    
    try:
        new_camper = Camper(
            name=data.get('name'),
            age=data.get('age')
        )
        
        db.session.add(new_camper)
        db.session.commit()
        
        return jsonify({
            'id': new_camper.id,
            'name': new_camper.name,
            'age': new_camper.age
        }), 201
        
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

#update camper using PATCH
@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = Camper.query.get(id)
    
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    #data from request
    data = request.get_json()
    #if  there is name or age in data, update the camper
    try:
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
        
        db.session.commit()
        
        return jsonify({
            'id': camper.id,
            'name': camper.name,
            'age': camper.age
        }), 202
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

#list all activities using GET
@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'difficulty': a.difficulty
    } for a in activities]), 200

#delete activity using DELETE
@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    
    db.session.delete(activity)
    db.session.commit()
    
    return '', 204 #no content after deletion

#create new signup
@app.route('/signups', methods=['POST'])
def create_signup():
    data = request.get_json()
    
    try:
        new_signup = Signup(
            camper_id=data.get('camper_id'),
            activity_id=data.get('activity_id'),
            time=data.get('time')
        )
        #save to db
        db.session.add(new_signup)
        db.session.commit()
        #construct response with camper and activity details
        response = {
            'id': new_signup.id,
            'camper_id': new_signup.camper_id,
            'activity_id': new_signup.activity_id,
            'time': new_signup.time,
            'activity': {
                'id': new_signup.activity.id,
                'name': new_signup.activity.name,
                'difficulty': new_signup.activity.difficulty
            },
            'camper': {
                'id': new_signup.camper.id,
                'name': new_signup.camper.name,
                'age': new_signup.camper.age
            }
        }
        #return 201 status code when created
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)




