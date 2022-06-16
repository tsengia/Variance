"""
Module for representing and evaluating calculated values.
"""

from variance.extensions import db
from variance.models.tracker import TrackerEntryModel
from sqlalchemy import select
import logging as logger

# This is for dynamically calculated measures.
# For example: 90% of 1 rep max, or 1/2 the pace of the PR time, etc.
class LambdaModel(db.Model):
    """
    A LambdaModel represents a value that can be calculated based off of
    already existing database data and how to calculate it.
    For example, 50% of 1 rep max would be represented as a LambdaModel
    """
    __tablename__ = "LambdaIndex"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    "Display name of this lambda function, for example: 'Percentage of 1 Rep Max'"

    function_name = db.Column(db.String(40), nullable=False)
    "Callable/internal name of this lambda function, for example 'percent_1rm'"

    def __str__(self) -> str:
        return "LambdaModel (%i): %s - %s" % (self.id,
                                              self.name, self.function_name)


def variance_evaluate_lambda(
        lambda_model,
        dimension,
        user_model,
        float_param,
        tracker_param):
    if lambda_model.function_name == "latest_percentage":
        if tracker_param is None or float_param is None:
            # TODO: Log this error
            logger.getLogger("variance").warning(
                "Lambda evaluated missing a parameter!")
            return None

        latest = select(TrackerEntryModel).where(
            TrackerEntryModel.parent_tracker_id == tracker_param.id).order_by(
            TrackerEntryModel.time).first()
        if latest is None:
            # TODO: Log this error
            return None

        # TODO: Make actual evaluation, and also return a unit
        return (latest.value * float_param, latest.unit)
    if lambda_model.function_name == "average_percentage":
        if tracker_param is None or float_param is None:
            return None
        return 1  # TODO: Make actual evaluation, and also return a unit
