===========================
Variance Permissions Model
===========================

Before attempting an API action through a public endpoint, Variance
performs an authorization check on the current user and the resource they
are attempting to perform the action on.

-----------------------------
PermissionModel
-----------------------------
Each :py:class:`~variance.models.permissions.PermissionModel` represents one *authorization* *rule*.

An authorization rule is explicitly tied to one API action.
An API action is identified by an action string.

The action string takes the following format:
``resource.action``  
Where ``resource`` is the name of the resource or resource collection being actioned on, and ``action`` is the action that is being performed. 

Examples of actions include:

*  ``new`` - Creating a new resource (``POST``)
*  ``update`` - Updating/patching an existing resource (``PUT``)
*  ``delete`` - Deleting an existing resource (``DELETE``)
*  ``view`` - Viewing/fetching an existing resource (``GET``)

Each :py:class:`~variance.models.permissions.PermissionModel` has the following settings that are evaluated in the following order:

1. ``force_public`` - If set to ``True``, then all users (logged in or not logged in) can perform the action.
2. ``allow_user`` - If the ID of the user attempting to perform the action matches the ID of the value of the ``allow_user`` column, then the action is permitted.
3. ``allow_role`` - If the role of the user attempting to perform the action matches the value of the ``allow_role`` column, then the action is permitted.
4. ``allow_owner`` - If this is set to ``True``, then the ID of the owner of the resource will be checked against the ID of the user attempting to perform the action.
5. ``check_public`` - If this is set to ``True``, then the ``is_public`` attribute of the model will determine if the action can be performed. If the model has ``is_public`` set to ``True``, then the action will be performed.

.. note::
    The ``force_public`` flag is mainly used for handling permissions for resources that do not have a well defined owner, such as UnitModels, ExerciseModels, and EquipmentModels.

    The ``check_public`` and ``is_public`` flags are mainly used for allowing users to set their Recipes, Consumables, and Workouts to be viewed publicly.

---------------------------
Resource Ownership
---------------------------
Some types of resources have a well-defined owner. For example, each :py:class:`~variance.models.tracker.TrackerModel` is owned by the user that created it.
However, there are some resources that do not have a well-defined owner.
For examples, :py:class:`~variance.models.muscle.MuscleModel`\s and :py:class:`~variance.models.muscle.MuscleGroupModel`\s do not have a well-defined owner as they are only created by the admin and cannot be modified through the API. All users can view these resources but cannot modify them.

Models that have a well-defined owner have their static ``has_owner()`` method set to return ``True``. If a Model does not have a well-defined owner, then ``has_owner()`` will return false.

Below is a list of Models that have a well-defined owner:

*  ConsumableModel
*  ConsumedEntryModel
*  GymModel
*  MealModel
*  MealPlanModel
*  MealPlanDayModel
*  RecipeModel
*  SetEntryModel
*  SetPlanModel
*  TrackerModel
*  TrackerEntryModel
*  WorkoutModel
*  WorkoutProgramModel
*  UserModel

--------------------------------
Heirarchial Ownership
--------------------------------
Certain Variance resources have a well defined-owner, but do not keep track of the owner in their own Model, but instead deffer ownership checks to the *parent Model*. The parent Model may also deffer ownership checks to another parent model, leading to a heirarchial tree of ownership checks until a root model is reached that doesn't deffer the ownership check.

Below is a list of Models that deffer their ownership:

*  ``SetPlanModel -> WorkoutModel -> WorkoutProgramModel``
*  ``MealModel -> MealPlanDayModel -> MealPlanModel``

For example, a user attempts to update a ``MealModel``, so an authorization check is performed. The authorization check starts at the ``MealModel``, which then calls for an authorization check on the ``MealPlanDayModel`` that is the owner of that ``MealModel``. The ``MealPlanDayModel`` then performs an authorization check on the ``MealPlanModel`` that owns it. If the authorization check on the ``MealPlanModel`` succeeds, then the user will be authorized to perform the update on the ``MealModel``.

.. note::
    Ownership checks and defferring ownership checks are performed through the ``check_owner()`` method.

