## ExerciseModel
`ExerciseIndex`
`id`
`canonical_name`
`name`
`description`
`use_duration`
`use_distance`
`use_weight`
`equipment` <-> ExerciseEquipmentList
`parent_exercise_id` -> `parent_exercise` <- `variations`
`has_owner()` - False
`__str__()`

## ExerciseEquipmentAssociation
`ExerciseEquipmentList`
`equipment_id` -> `equipment`
`exercise_id` -> `exercise`
`__str__()`
