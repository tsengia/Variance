import pytest

from variance.models.global_setting import GlobalSettingModel
from variance.schemas.global_setting import GlobalSettingSchema, parse_setting_value

from marshmallow import ValidationError

def test_boolean_validation():
    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"boolean","value":"asdf","display_name":"AUGH"}'
        g = GlobalSettingSchema()
        g.loads(a)

    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"boolean","value":"","display_name":"asd"}'
        g = GlobalSettingSchema()
        g.loads(a)

    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"boolean","value":"7","display_name":"1"}'
        g = GlobalSettingSchema()
        g.loads(a)

    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"boolean","value":"nope","display_name":"AfvdfvUGH"}'
        g = GlobalSettingSchema()
        g.loads(a)

    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"boolean","value":"yeah","display_name":"AfvdfvUGH"}'
        g = GlobalSettingSchema()
        g.loads(a)

    g = GlobalSettingSchema()

    a = '{"name":"test","type_hint":"boolean","value":"True","display_name":"AfvdfvUGH"}'
    d = g.loads(a)
    assert(parse_setting_value(d) == True)
    assert(d["name"] == "test")

    a = '{"name":"test","type_hint":"boolean","value":"False","display_name":"AfvdfvUGH"}'
    d = g.loads(a)
    assert(parse_setting_value(d) == False)

def test_float_validation():
    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"float","value":"abcde","display_name":"AfvdfvUGH"}'
        g = GlobalSettingSchema()
        g.loads(a)

    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"float","value":"","display_name":"AfvdfvUGH"}'
        g = GlobalSettingSchema()
        g.loads(a)

    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"float","value":"--1","display_name":"AfvdfvUGH"}'
        g = GlobalSettingSchema()
        g.loads(a)

    with pytest.raises(ValidationError):
        a = '{"name":"test","type_hint":"float","value":"+1000","display_name":"AfvdfvUGH"}'
        g = GlobalSettingSchema()
        g.loads(a)

    a = '{"name":"test","type_hint":"float","value":"1.0","display_name":"AfvdfvUGH"}'
    g = GlobalSettingSchema()
    d = g.loads(a)
    assert(parse_setting_value(d) == 1.0)

    a = '{"name":"test","type_hint":"float","value":"0","display_name":"AfvdfvUGH"}'
    d = g.loads(a)
    assert(parse_setting_value(d) == 0.0)

    a = '{"name":"test","type_hint":"float","value":"-200000","display_name":"AfvdfvUGH"}'
    d = g.loads(a)
    assert(parse_setting_value(d) == -200000.0)