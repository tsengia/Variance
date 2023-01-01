from variance.extensions import db, ResourceBase

class GlobalSettingModel(ResourceBase):
    __tablename__ = "GlobalSettingsIndex"

    name = db.Column(db.String(30), nullable=False, unique=True)
    "Internal name of this setting. Example: 'allow_registration'"

    display_name = db.Column(db.String(40), nullable=False)
    "Diplay name of this setting. Example: 'Allow New User Registration'"

    type_hint = db.Column(db.String(20), nullable=False)
    "Datatype that this setting is."

    value = db.Column(db.String(40), nullable=False)
    "Value that this setting is set to"

    @staticmethod
    def get_uuid_by_name(text):
        name_match = GlobalSettingsModel.query.filter_by(name=text).first()
        if name_match:
            return name_match.uuid

    def __str__(self):
        return "GlobalSettingsModel (%s): %s = %s (%s)" % (
            self.uuid, self.name, self.value, self.type_hint)
