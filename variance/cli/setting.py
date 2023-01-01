from variance.models.global_setting import GlobalSettingModel
from variance.models.user_setting import UserSettingModel
from variance.schemas.global_setting import GlobalSettingSchema
from variance.schemas.user_setting import UserSettingSchema
from variance.cli.resource import ResourceCLI

from flask.cli import AppGroup

setting_cli = AppGroup("settings")
global_setting_cli = ResourceCLI(GlobalSettingModel, GlobalSettingSchema, "GlobalSettings", "global")
user_setting_cli = ResourceCLI(UserSettingModel, UserSettingSchema, "UserSettings", "user")

global_setting_cli.attach(setting_cli)
user_setting_cli.attach(setting_cli)