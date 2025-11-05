from app import app
from database import db
from models import Camper, Activity, Signup

def seed_data():
    with app.app_context():
        #clear existing data
        Signup.query.delete()
        Camper.query.delete()
        Activity.query.delete()
        
        #create campers
        campers = [
            Camper(name="Mitchelle Marani", age=10),
            Camper(name="Amina Njoroge", age=16),
            Camper(name="John Otieno", age=12),
            Camper(name="David Omache", age=14),
            Camper(name="Sarah Nanjala", age=9)
        ]
        db.session.add_all(campers)
        db.session.commit()
        
        #create activities
        activities = [
            Activity(name="Safari Walk", difficulty=3),
            Activity(name="Ngong Hills Hike", difficulty=4),
            Activity(name="Lake Naivasha Boat Ride", difficulty=2),
            Activity(name="Campfire storytelling", difficulty=1),
            Activity(name="Bungee Jumping", difficulty=4),
            Activity(name="Rock Climbing", difficulty=5),
            Activity(name="Bush breakfast", difficulty=1)
        ]
        db.session.add_all(activities)
        db.session.commit()
        
        #create signups
        signups=[
            Signup(camper_id=3, activity_id=5, time=8),
            Signup(camper_id=3, activity_id=7, time=1),
            Signup(camper_id=4, activity_id=3, time=9),
            Signup(camper_id=1, activity_id=1, time=10),
            Signup(camper_id=2, activity_id=2, time=14)   
        ]
        db.session.add_all(signups)
        db.session.commit()
        
if __name__ == '__main__':
    seed_data()