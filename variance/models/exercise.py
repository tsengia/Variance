from datetime import datetime

from variance import db 

class ExerciseModel(db.Model):
    __tablename__ = "ExerciseIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the exercise
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Is this exercise measured in time?
    use_duration = db.Column(db.Boolean, nullable=False, default=0)

    # Is this exercise measured in distance?
    use_distance = db.Column(db.Boolean, nullable=False, default=0)

    # Is this exercise measured in weight?
    use_weight = db.Column(db.Boolean, nullable=False, default=0)

    # What piece of equipment does this exercise use?
    equipment_id = db.Column(db.Integer, db.ForeignKey("EquipmentIndex.id"), nullable=True)
    equipment = db.relationship("EquipmentModel")

    # Is this exercise a variation of another exercise, if so, which exercise? (Ex: Close grip bench is a variation of bench press)
    parent_exercise_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), nullable=True)
    parent_exercise = db.relationship("ExerciseModel", foreign_keys="ExerciseModel.parent_exercise_id", back_populates="variations")
    variations = db.relationship("ExerciseModel")

    def __str__(self):
        return "%u Exercise: %s dur(%s), dis($s), wght(%s), equip(%s)" % (self.id, self.name, str(self.use_duration), str(self.use_distance), str(self.use_weight), str(self.equipment.name))

    @staticmethod
    def has_owner():
        return False

    def __str__(self):
        return "%u ExerciseModel: %s" % (self.id, self.name)