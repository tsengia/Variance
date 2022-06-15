## MuscleModel
Table: `MuscleIndex`  
`id`  
`name`  
`short_name`  
`diagram_id`  
`groups` <-> MuscleGroupAssociation  
`has_owner()` - False    
`__str__()`  

## MuscleGroupModel
Table: `MuscleGroupIndex`  
`id`   
`canonical_name`  
`name`  
`description`  
`muscles` <-> MuscleGroupAssociation  
`has_owner()` - False  
`__str__()`  

## MuscleGroupAssociation
Table: `MuscleGroupAssociation`  
`group_id`  
`muscle_id`  
`__str__()`   
