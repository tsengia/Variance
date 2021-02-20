DEFAULT_PERMISSIONS=[
# Units
{ "endpoint": "unit", "methods": ["new","update","delete"], "roles": ["admin"] },
{ "endpoint": "unit", "methods": ["view"], "force_public": True },
# Trackers
{ "endpoint": "tracker", "methods": ["new","update","delete"], "roles": ["admin"] },
{ "endpoint": "tracker", "methods": ["view"], "roles": ["user"] },
# Tracker Entries
{ "endpoint": "tracker_entry", "methods": ["new"], "roles": ["user"] },
{ "endpoint": "tracker_entry", "methods": ["view", "update", "delete"], "check_owner": True },
# Equipment
{ "endpoint": "equipment", "methods": ["new","update","delete"], "roles": ["admin"] },
{ "endpoint": "equipment", "methods": ["view"], "force_public": True },
# "Muscles
{ "endpoint": "muscle", "methods": ["new","update","delete"], "roles": ["admin"] },
{ "endpoint": "muscle", "methods": ["view"], "force_public": True },
# Muscle Groups
{ "endpoint": "muscle_group", "methods": ["new","update","delete"], "roles": ["admin"] },
{ "endpoint": "muscle_group", "methods": ["view"], "force_public": True },
# Nutrients
{ "endpoint": "nutrient", "methods": ["new","update","delete"], "roles": ["admin"] },
{ "endpoint": "nutrient", "methods": ["view"], "force_public": True },
# Consumables, admins can do anything, users can do anything to their own, non-users can view if public
{ "endpoint": "consumable", "methods": ["new"], "roles": ["user","admin"] },
{ "endpoint": "consumable", "methods": ["view"], "roles": ["admin"], "owner":True, "check_public":True},
{ "endpoint": "consumable", "methods": ["update","delete"], "roles": ["admin"], "owner":True, "check_public":False},
# Recipes
{ "endpoint": "recipe", "methods": ["new"], "roles": ["user","admin"] },
{ "endpoint": "recipe", "methods": ["view"], "roles": ["admin"], "owner":True, "check_public":True },
{ "endpoint": "recipe", "methods": ["update","delete"], "roles": ["admin"], "owner":True, "check_public":False },

]