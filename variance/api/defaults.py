import json
import pathlib

from variance.models.unit import UnitModel

class DefaultSettingsManager:

    def populate_user_with_defaults(self, user):
        unit_defaults = self._user_defaults["units"]
        user.exercise_weight_unit_id = unit_defaults["exercise_weight_unit_id"]
        user.exercise_distance_unit_id = unit_defaults["exercise_distance_unit_id"]
        user.food_weight_unit_id = unit_defaults["food_weight_unit_id"]
        user.food_volume_unit_id = unit_defaults["food_volume_unit_id"]
        user.body_weight_unit_id = unit_defaults["body_weight_unit_id"]
        user.body_distance_large_unit_id = unit_defaults["body_distance_large_unit_id"]
        user.body_distance_small_unit_id = unit_defaults["body_distance_small_unit_id"]


    def __init__(self, defaults_path):
        self._defaults_path = defaults_path
        print("DefaultSettingsManager constructed")
        self._user_defaults = json.load((defaults_path / "user.json").open("r"))
        unit_defaults = self._user_defaults["units"]
        self._user_defaults["units"]["exercise_weight_unit_id"] = UnitModel.get_id_by_abbreviation(unit_defaults["exercise_weight_unit"])
        self._user_defaults["units"]["exercise_distance_unit_id"] = UnitModel.get_id_by_abbreviation(unit_defaults["exercise_distance_unit"])
        self._user_defaults["units"]["food_weight_unit_id"] = UnitModel.get_id_by_abbreviation(unit_defaults["food_weight_unit"])
        self._user_defaults["units"]["food_volume_unit_id"] = UnitModel.get_id_by_abbreviation(unit_defaults["food_volume_unit"])
        self._user_defaults["units"]["body_weight_unit_id"] = UnitModel.get_id_by_abbreviation(unit_defaults["body_weight_unit"])
        self._user_defaults["units"]["body_distance_large_unit_id"] = UnitModel.get_id_by_abbreviation(unit_defaults["body_distance_large_unit"])
        self._user_defaults["units"]["body_distance_small_unit_id"] = UnitModel.get_id_by_abbreviation(unit_defaults["body_distance_small_unit"])

