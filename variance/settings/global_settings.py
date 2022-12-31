from variance.extensions import db

from variance.settings.key_value_model import define_key_value_model

global_unit_settings = \
    define_key_value_model(\
        db.ForeignKey("UnitIndex.uuid", ondelete="CASCADE"),\
        "global_unit_settings")

global_number_settings = \
    define_key_value_model(\
        db.Float(), "global_number_settings")

global_string_settings = \
    define_key_value_model(\
        db.String(length=40), "global_string_settings")

global_boolean_settings = \
    define_key_value_model(\
        db.Boolean(), "global_boolean_settings")

global_settings_keys = {
    "default_distance_unit":    "unit",
    "default_weight_unit":      "unit",
    "default_duration_unit":    "unit",
    "allow_registration":       "boolean",
    "string_test":              "string",
    "number_test":              "number"
}

global_settings_types = {
    "unit":     global_unit_settings,
    "boolean":  global_boolean_settings,
    "number":   global_number_settings,
    "string":   global_string_settings
}

def get_global_setting(key: str):
    "Returns the value of a global setting"
    if not key in global_settings_keys:
        return None
    model = global_settings_types[global_settings_keys[key]].get(key)
    return str(model.value)

def set_global_setting(key: str, value):
    "Sets a global settings value, returns True on success"
    if not key in global_settings_keys:
        return False
    model = global_settings_types[global_settings_keys[key]].get(key)
    model.value = value
    return True