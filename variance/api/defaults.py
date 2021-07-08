import json
import pathlib

from variance import db
from variance.models.units import UnitModel

class DefaultSettingsManager

    def populate_user_with_defaults(self, user):
        pass

    def __init__(self, defaults_path):
        self.defaults_path_ = defaults_path

        self.user_defaults_ = json.load((defaults_path / "user.json").open("r"))
