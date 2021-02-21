from variance import db 

# This is for dynamically calculated measures.
# For example: 90% of 1 rep max, or 1/2 the pace of the PR time, etc.
class LambdaModel(db.Model):
    __tablename__ = "LambdaIndex"
    
    id = db.Column(db.Integer, primary_key=True)

    # Name of this lambda function, for example: "Percentage of 1 Rep Max"
    name = db.Column(db.String(100), nullable=False)
    
    # Callable/internal name of this lambda function, for example "percent_1rm"
    function_name = db.Column(db.String(40), nullable=False)
    
def variance_evaluate_lambda(lambda_model, user_model, lambda_param1, lambda_param2, lambda_param3, lambda_exercise_param1, lambda_tracker_param1):
    if lambda_model.function_name == "max":
        return 1 # TODO: Make actual evaluation, and also return a unit