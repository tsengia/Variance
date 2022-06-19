===========================
Variance Permissions Model
===========================

Before attempting an API action through a public endpoint, Variance
performs an authorization check on the current user and the resource they
are attempting to perform the action on.

---------------------------
Resource Ownership
---------------------------
Some types of resources have a well-defined owner. For example, each TrackerModel is owned by the user that created it.
However, there are some resources that do not have a well-defined owner.
For examples, MuscleModels and MuscleGroupModels do not have a well-defines owner as they are only created by the admin and cannot be modified through the API. All users can view these resources but cannot modify them.

Models that have a well-defined owner have their static ``has_owner()`` method set to return ``True``. If a Model does not have a well-defined owner, then ``has_owner()`` will return false.

Below is a list of Models that have a well-defined owner:
* ConsumableModel
* ConsumedEntryModel
* GymModel
* MealModel
* MealPlanModel
* MealPlanDayModel
* RecipeModel
* SetEntryModel
* SetPlanModel
* TrackerModel
* TrackerEntryModel
* WorkoutModel
* WorkoutProgramModel
* UserModel

-----------------------------
PermissionModel
-----------------------------
Each ``PermissionModel`` represents one *authorizatoin\ rule*.
An authrozation rule is explicitly tied to one API action.
An API action is identified by an action string.
The action string takes the following format:
``resource.action``  
Where ``resource`` is the name of the resource or resource collection being actioned on, and ``action`` is the action that is being performed. 

Examples of actions include:
* ``new`` - Creating a new resource (``POST``)
* ``update`` - Updating/patching an existing resource (``PUT``)
* ``delete`` - Deleting an existing resource (``DELETE``)
* ``view`` - Viewing/fetching an existing resource (``GET``)

