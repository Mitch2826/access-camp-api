from sqlalchemy.orm import validates

from server.database import db

#camper model
class Camper(db.Model):
    __tablename__='campers'
    
    #columns
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    #relationship with signup
    signups = db.relationship('Signup', backref='camper', cascade='all, delete-orphan')
    
    #validation for name
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        return name
    
    #validation for age
    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int) or age < 8 or age > 18:
            raise ValueError("Age must be an integer between 8 and 18")
        return age
    
    def __repr__(self):
        return f"<Camper id={self.id} name={self.name} age={self.age}>"
    
#activity model
class Activity(db.Model):
    __tablename__='activities'
    
    #columns
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    
    #relationship 
    signups = db.relationship('Signup', backref='activity', cascade='all, delete-orphan')
    
    #validation for name
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        return name
    
    #validation for difficulty
    @validates('difficulty')
    def validate_difficulty(self, key, difficulty):
        if not isinstance(difficulty, int) or difficulty < 1 or difficulty > 5:
            raise ValueError("Difficulty must be an integer between 1 and 5")
        return difficulty
    
    def __repr__(self):
        return f"<Activity id={self.id} name={self.name} difficulty={self.difficulty}>"
    
#signup model
class Signup(db.Model):
    __tablename__='signups'
    
    #columns
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    
    #foreign keys
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    
    #validation for time
    @validates('time')
    def validate_time(self, key, time):
        if not isinstance(time, int) or time < 0 or time > 23:
            raise ValueError("Time must be an integer between 0 and 23")
        return time
    
    def __repr__(self):
        return f"<Signup id={self.id} time={self.time} camper_id={self.camper_id} activity_id={self.activity_id}>"