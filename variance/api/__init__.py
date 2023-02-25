"""
Module containing API endpoints.
"""
from flask import Blueprint
from . import auth
from . import units
from . import equipment
from . import exercises
from . import muscles
from . import trackers
from . import nutrients
from . import recipes
from . import consumables
from . import settings