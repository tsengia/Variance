===========================
Gyms & Equipment
===========================
Variance allows users to track types of exercise equipment
available and which gyms that equipment is located.
This can be useful for the generation of exercise routines
that are constrained by lack of equipment.

:py:class:`~variance.models.equipment.EquipmentModel`\s represent a
piece of equipment. They do not have an owner, and can be viewed by
all users.  

Variance recommends that all ``EquipmentModel``\s be manufacturer agnostic.  
This is to prevent overwhelming the user and generation algorithms with too
many choices. So if a cable machine by manufacturer A can perform the same
exercises as cable machine by manufacturer B, then there should only be one
``EquipmentModel`` that represents both of them.

A :py:class:`~variance.models.gym.GymModel`` is a collection of ``EquipmentModel``\s. A ``GymModel`` **does NOT** own any ``EquipmentModel``\s; they are only *associated* together in a Many-to-Many relationship. There can be multiple gyms, and each gym can be associated with multiple pieces of equipment.
