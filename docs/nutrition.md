## NutrientInfoModel
Table: `NutrientInfoIndex`
`id`
`canonical_name`
`name`
`scientific_name`
`abbreviation`
`description`
`is_amino_acid`
`is_element`
`is_vitamin`
`vitamin_family`
`vitamin_number`
`wikipedia_link`
`fdc_nid`
`fndds`
`has_owner()` - False
`get_tags()`
`__str__()`

## RecipeModel
Table: `RecipeIndex`
`id`
`canonical_name`
`name`
`created_date`
`description`
`instructions`
`attribution`
`author`
`is_public`
`owner_id` -> `owner`
`ingredients` <-> RecipeIngredientList
`products` <-> RecipeProductsList
`has_owner()` - True
`check_owner(id)`
`__str__()`

## ConsumableModel
Table: `ConsumableIndex`
`id`
`canonical_name`
`name`
`created_date`
`description`

`is_generic`
`is_branded`
`generic_food_id` -> `generic_food`
`is_ingredient`
`is_snack`
`is_recipe`
`is_entree`
`is_side`
`is_fruit`
`is_vegetable`
`is_meat`
`is_soup`

`owner_id` -> `owner`
`is_public`

`calories`
`protein`
`carbohydrates`
`fat`

`closed_shelf_life`
`opened_shelf_life`
`freezer_life`
`is_packaged`
`cost_per_package`
`servings_per_package`


`has_peanuts`
`has_treenuts`
`has_dairy`
`has_eggs`
`has_pork`
`has_beef`
`has_meat`
`has_fish`
`has_shellfish`
`has_gluten`
`is_vegetarian`
`is_vegan`
`is_kosher`


`fdc_id`
`fndds_id`
`wweia_category`
`upc`
`upc_a`
`upc_c`
`ean_8`
`ean_13`

`data_source`
`attribution`

`has_owner()` - True
`check_owner(id)`
`__str__()`

