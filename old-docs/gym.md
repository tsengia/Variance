## GymModel
Table: `GymIndex`  
`id`  
`name`  
`location`  
`description`  
`is_public`  
`owner_id` => `owner`  
`equipment` <-> GymEquipmentList  
`has_owner()` - True   
`check_owner(id)`  
`__str__()`  

### GymEquipmentAssociation
Table: `GymEquipmentList`  
`equipment_id` -> `equipment`  
`gym_id` -> `gym`  
`__str__()`  
