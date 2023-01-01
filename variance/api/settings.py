from variance.models.global_setting import GlobalSettingModel
from variance.models.user_setting import UserSettingModel
from variance.schemas.global_setting import GlobalSettingSchema
from variance.schemas.user_setting import UserSettingSchema
from variance.api.resource_api import VarianceResource

global_settings_endpoint = VarianceResource(GlobalSettingModel, GlobalSettingSchema, __name__, "settings/global")
user_settings_endpoint = VarianceResource(UserSettingModel, UserSettingSchema, __name__, "settings/user")