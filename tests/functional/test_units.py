import pytest

from variance.models.unit import UnitModel

def test_default_units(app_with_defaults, client):
    r = client.get("/api/units/")
    assert r.status_code == 200

def test_find_by_abbreviation(app_with_defaults):
    assert(UnitModel.get_uuid_by_abbreviation("s") != None)
    assert(not UnitModel.get_uuid_by_abbreviation("FOOBAR"))
    assert(not UnitModel.get_uuid_by_abbreviation("FOOBAZ"))
    assert(not UnitModel.get_uuid_by_abbreviation(""))
    assert(not UnitModel.get_uuid_by_abbreviation("1"))
    assert(not UnitModel.get_uuid_by_abbreviation("0"))
    assert(not UnitModel.get_uuid_by_abbreviation("s.kjfbq379p4y8t 'p;oqf.kjgbaeipl7rghq[9oigb/dlaksb"))
    assert(UnitModel.get_uuid_by_abbreviation("mi") != None)
    assert(UnitModel.get_uuid_by_abbreviation("km") != None)
    assert(UnitModel.get_uuid_by_abbreviation("lb") != None)
    assert(UnitModel.get_uuid_by_abbreviation("g") != None)
    assert(UnitModel.get_uuid_by_abbreviation("kg") != None)

def test_find_by_name(app_with_defaults):
    assert(UnitModel.get_uuid_by_name("meters"))
    assert(UnitModel.get_uuid_by_name("feet"))
    assert(UnitModel.get_uuid_by_name("pounds"))
    assert(UnitModel.get_uuid_by_name("kilograms"))
    assert(UnitModel.get_uuid_by_name("minutes"))
    assert(not UnitModel.get_uuid_by_name("foo"))
    assert(not UnitModel.get_uuid_by_name("''asd"))
    assert(not UnitModel.get_uuid_by_name(""))
    assert(not UnitModel.get_uuid_by_name("1"))
    assert(not UnitModel.get_uuid_by_name("1=1"))
    assert(not UnitModel.get_uuid_by_name("0"))
    assert(not UnitModel.get_uuid_by_name("1=1;"))
    assert(not UnitModel.get_uuid_by_name("s.kjfbq379p4y8t 'p;oqf.kjgbaeipl7rghq[9oigb/dlaksb"))