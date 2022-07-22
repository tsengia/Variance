from datetime import datetime, date
from werkzeug.security import check_password_hash, generate_password_hash

from variance.extensions import db


class UserModel(db.Model):
    __tablename__ = "UserIndex"

    id = db.Column(db.Integer, primary_key=True)
    # Management Info
    username = db.Column(db.String(30), unique=True, nullable=False)

    # Email address of the user. NOTE: Can be NULL!
    email = db.Column(db.String(80), nullable=True)

    # Password hash of the user.
    password = db.Column(db.String(128), nullable=False)

    # Date this user was born. Used for calculating age.
    birthdate = db.Column(db.Date(), nullable=False)

    # Datetime this user was created.
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now())

    # User role. Current values: "user", "admin"
    role = db.Column(db.String(10), nullable=False, default="user")

    # User Data
    # List of trackers this user has running
    trackers = db.relationship(
        "TrackerModel", back_populates="owner", cascade="all, delete")

    # List of nutritional items created by this user
    consumables = db.relationship(
        "ConsumableModel", back_populates="owner", cascade="all, delete")
    recipies = db.relationship(
        "RecipeModel", back_populates="owner", cascade="all, delete")
    mealplans = db.relationship(
        "MealPlanModel", back_populates="owner", cascade="all, delete")

    set_entries = db.relationship(
        "SetEntryModel", back_populates="owner", cascade="all, delete")
    consumption_entries = db.relationship(
        "ConsumedEntryModel", back_populates="owner", cascade="all, delete")
    programs = db.relationship(
        "WorkoutProgramModel", back_populates="owner", cascade="all, delete")
    
    # Diet Settings
    # Can this user not eat peanuts? (setting to True means that no recipies
    # containing peanuts will be suggested)
    no_peanuts = db.Column(db.Boolean, nullable=True)

    # Can this user not eat treenuts?
    no_treenuts = db.Column(db.Boolean, nullable=True)

    # Can this user not eat dairy?
    no_dairy = db.Column(db.Boolean, nullable=True)

    # Can this user not eat eggs?
    no_eggs = db.Column(db.Boolean, nullable=True)

    # Can this user not eat pork?
    no_pork = db.Column(db.Boolean, nullable=True)

    # Can this user not eat beef (cow)?
    no_beef = db.Column(db.Boolean, nullable=True)

    # Can this user not eat meat?
    no_meat = db.Column(db.Boolean, nullable=True)

    # Can this user not eat fish?
    no_fish = db.Column(db.Boolean, nullable=True)

    # Can this user not eat shellfish?
    no_shellfish = db.Column(db.Boolean, nullable=True)

    # Can this user not eat gluten?
    no_gluten = db.Column(db.Boolean, nullable=True)

    # Does this user require vegetarian only foods?
    is_vegetarian = db.Column(db.Boolean, nullable=True)

    # Does this user require vegan only foods?
    is_vegan = db.Column(db.Boolean, nullable=True)

    # Does this user require kosher only foods?
    is_kosher = db.Column(db.Boolean, nullable=True)

    # Returns the age (in years) of this user. Integer, not a fraction
    def age(self):
        bday = datetime.date(self.birthdate)
        today = date.today()
        return today.year - bday.year - \
            ((today.month, today.day) < (bday.month, bday.day))

    def get_tags(self):
        tags = []
        if self.no_pork:
            tags.append("nopork")
        if self.no_meat:
            tags.append("nomeat")
        if self.no_fish:
            tags.append("nofish")
        if self.no_shellfish:
            tags.append("noshellfish")
        if self.no_beef:
            tags.append("nobeef")
        if self.no_dairy:
            tags.append("nodairy")
        if self.no_eggs:
            tags.append("noeggs")
        if self.no_peanuts:
            tags.append("nopeanuts")
        if self.no_gluten:
            tags.append("nogluten")
        if self.no_treenuts:
            tags.append("notreenuts")
        if self.is_vegan:
            tags.append("vegan")
        if self.is_vegetarian:
            tags.append("vegetarian")
        if self.is_kosher:
            tags.append("kosher")
        return tags

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
