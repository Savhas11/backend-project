from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20),nullable=False, default="user")
    email = db.Column(db.String,nullable=False, unique=True)
    password_hash = db.Column(db.String(256),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False)
    trails = db.relationship("Trail", back_populates="user")

class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    distance_miles = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    user = db.relationship("User", back_populates="trails")

