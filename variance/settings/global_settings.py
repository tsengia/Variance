import variance.settings.settings_model

global_settings_keys = [
"default_distance_unit":"unit",
"default_weight_unit":"unit",
"default_duration_unit":"unit",
"allow_registration":"boolean",
"string_test":"string",
"number_test":"number"
]

global_settings_types = {
    "unit": global_unit_settings,
    "boolean":global_boolean_settings,
    "number":global_number_settings,
    "string":global_string_settings
}

def get_global_value(key: str):
    "Returns the value of a global setting"
    if not key in global_settings_keys:
        return None
    model = global_settings_types[global_settings_keys[key]].get(key)
    return str(model.value)

def set_global_value(key: str, value):
    "Sets a global settings value, returns True on success"
    if not key in global_settings_keys:
        return False
    model = global_settings_types[global_settings_keys[key]].get(key)
    model.value = value
    return True
