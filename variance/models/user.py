from datetime import datetime, date
from werkzeug.security import check_password_hash, generate_password_hash

from variance import db

class UserModel(db.Model):
    __tablename__ = "UserIndex"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    
    # Email address of the user. NOTE: Can be NULL!
    email = db.Column(db.String(80), nullable=True)
    
    # Password hash of the user.
    password = db.Column(db.String(128), nullable=False)
    
    # Date this user was born. Used for calculating age.
    birthdate = db.Column(db.Date(), nullable=False)
    
    # Datetime this user was created.
    created_on = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    
    # User role. Current values: "user", "admin"
    role = db.Column(db.String(10), nullable=False, default="user")

    # List of trackers this user has running
    trackers = db.relationship("TrackerModel", back_populates="user", cascade="all, delete")

    # List of nutritional items created by this user
    consumables = db.relationship("ConsumableModel", back_populates="created_by", cascade="all, delete")
    recipies = db.relationship("RecipieModel", back_populates="created_by", cascade="all, delete")
    ingredients = db.relationship("IngredientModel", back_populates="created_by", cascade="all, delete")
    mealplans = db.relationship("MealPlanModel", back_populates="created_by", cascade="all, delete")

    
    # Returns the age (in years) of this user. Integer, not a fraction
    def age(self):
        bday = datetime.date(self.birthdate)
        today = date.today()
        return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)