# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2019  GridMarkets
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####
from gridmarkets_blender_addon.meta_plugin import utils
from gridmarkets_blender_addon.meta_plugin import User
from gridmarkets_blender_addon.meta_plugin.user_interface import UserInterface as MetaUserInterface
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon import constants, utils_blender

import bpy


class UserInterface(MetaUserInterface):

    # email
    def get_auth_email(self) -> str:
        return bpy.context.scene.props.user_interface.auth_email_input

    def set_auth_email(self, email: str) -> None:
        bpy.context.scene.props.user_interface.auth_email_input = email

    def get_auth_email_validity_flag(self) -> bool:
        return bpy.context.scene.props.user_interface.is_auth_email_valid

    def set_auth_email_validity_flag(self, is_valid: bool) -> None:
        bpy.context.scene.props.user_interface.is_auth_email_valid = is_valid

    def get_auth_email_validity_message(self) -> str:
        return bpy.context.scene.props.user_interface.auth_email_validity_message

    def set_auth_email_validity_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.auth_email_validity_message = message

    # access key
    def get_auth_access_key(self) -> str:
        return bpy.context.scene.props.user_interface.auth_access_key_input

    def set_auth_access_key(self, auth_access_key) -> None:
        bpy.context.scene.props.user_interface.auth_access_key_input = auth_access_key

    def get_auth_access_key_validity_flag(self) -> bool:
        return bpy.context.scene.props.user_interface.is_auth_access_key_valid

    def set_auth_access_key_validity_flag(self, is_valid: bool) -> None:
        bpy.context.scene.props.user_interface.is_auth_access_key_valid = is_valid

    def get_auth_access_key_validity_message(self) -> str:
        return bpy.context.scene.props.user_interface.auth_access_key_validity_message

    def set_auth_access_key_validity_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.auth_access_key_validity_message = message

    # user
    def get_user_validity_flag(self) -> bool:
        return bpy.context.scene.props.user_interface.is_user_valid

    def set_user_validity_flag(self, is_valid: bool) -> None:
        bpy.context.scene.props.user_interface.is_user_valid = is_valid

    def get_user_validity_message(self) -> str:
        return bpy.context.scene.props.user_interface.user_validity_message

    def set_user_validity_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.user_validity_message = message

    # operation
    def is_running_operation(self) -> bool:
        return bpy.context.scene.props.user_interface.is_running_operation

    def set_is_running_operation_flag(self, value: bool) -> None:
        bpy.context.scene.props.user_interface.is_running_operation = value

    def get_running_operation_message(self) -> str:
        return bpy.context.scene.props.user_interface.running_operation_message

    def set_running_operation_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.running_operation_message = message

    # load profile
    def load_profile(self, user_profile: User):
        bpy.context.scene.props.user_interface.auth_email_input = user_profile.get_auth_email()
        bpy.context.scene.props.user_interface.auth_access_key_input = user_profile.get_auth_key()

    # spinner
    def get_running_operation_spinner(self) -> int:
        return bpy.context.scene.props.user_interface.running_operation_spinner

    def increment_running_operation_spinner(self) -> None:
        bpy.context.scene.props.user_interface.running_operation_spinner += 1

        if bpy.context.scene.props.user_interface.running_operation_spinner > 7:
            bpy.context.scene.props.user_interface.running_operation_spinner = 0

    # logger
    def show_log_dates(self) -> bool:
        return bpy.context.scene.props.user_interface.show_log_dates

    def set_show_log_dates(self, enabled: bool) -> None:
        bpy.context.scene.props.user_interface.show_log_dates = enabled

    def show_log_times(self) -> bool:
        return bpy.context.scene.props.user_interface.show_log_times

    def set_show_log_times(self, enabled: bool) -> None:
        bpy.context.scene.props.user_interface.show_log_times = enabled

    def show_logger_names(self) -> bool:
        return bpy.context.scene.props.user_interface.show_logger_names

    def set_show_logger_names(self, enabled: bool) -> None:
        bpy.context.scene.props.user_interface.show_logger_names = enabled

    # console
    def is_logging_console_open(self) -> bool:
        return bpy.context.scene.props.is_logging_console_open

    def toggle_logging_console(self) -> None:
        bpy.context.scene.props.is_logging_console_open = not bpy.context.scene.props.is_logging_console_open

    # job preset
    def get_show_hidden_job_preset_attributes(self) -> bool:
        return bpy.context.scene.props.user_interface.show_hidden_job_preset_attributes

    def set_show_hidden_job_preset_attributes(self, value: bool) -> None:
        bpy.context.scene.props.user_interface.show_hidden_job_preset_attributes = value

    # project upload method
    def get_layout(self) -> str:
        return bpy.context.scene.props.user_interface.ui_layout

    def set_layout(self, value: str) -> None:
        bpy.context.scene.props.user_interface.ui_layout = value

    @staticmethod
    def reset_project_value() -> None:
        from types import SimpleNamespace
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher

        plugin = PluginFetcher.get_plugin()
        scene = bpy.context.scene
        project_attributes = getattr(scene, constants.PROJECT_ATTRIBUTES_POINTER_KEY)

        # get the name of all the remote projects in a SimpleNamespace object
        remote_projects = map(lambda remote_project: SimpleNamespace(name=remote_project.get_name()),
                              plugin.get_remote_project_container().get_all())

        default_name =  utils.create_unique_object_name(remote_projects, name_prefix=utils_blender.get_project_name())
        setattr(project_attributes, api_constants.ROOT_ATTRIBUTE_ID, default_name)

    @staticmethod
    def reset_product_value() -> None:
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_schema = plugin.get_api_client().get_cached_api_schema()

        product_attribute = api_schema.get_project_attribute_with_id(api_constants.PROJECT_ATTRIBUTE_IDS.PRODUCT)

        # set the product
        if bpy.context.scene.render.engine == constants.VRAY_RENDER_RT:
            product_attribute.set_value(api_constants.PRODUCTS.VRAY)
        else:
            product_attribute.set_value(api_constants.PRODUCTS.BLENDER)

    @staticmethod
    def reset_product_version_value() -> None:
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_schema = plugin.get_api_client().get_cached_api_schema()

        # attempt to reset the product version to the closest matching version
        # only do for blender versions
        value = utils_blender.get_closest_matching_product_version()
        if value is not None:
            blender_versions_attribute = api_schema.get_project_attribute_with_id(api_constants.BLENDER_VERSIONS_ENUM_ID)
            blender_versions_attribute.set_value(value)

    @staticmethod
    def reset_export_path() -> None:
        bpy.context.scene.props.export_path = utils.get_desktop_path()

    @staticmethod
    def get_export_path() -> str:
        return bpy.context.scene.props.export_path

    @staticmethod
    def reset_blend_file_path() -> None:
        if bpy.context.blend_data.is_saved:
            bpy.context.scene.props.blend_file_path = bpy.context.blend_data.filepath
        else:
            bpy.context.scene.props.blend_file_path = ""

    @staticmethod
    def get_blend_file_path() -> str:
        return bpy.context.scene.props.blend_file_path

    @staticmethod
    def reset_root_directory() -> None:
        bpy.context.scene.props.root_directory = ""

    @staticmethod
    def get_root_directory() -> str:
        return bpy.context.scene.props.root_directory

    @staticmethod
    def reset_upload_all_files_in_root() -> None:
        bpy.context.scene.props.upload_all_files_in_root = False

    @staticmethod
    def get_upload_all_files_in_root() -> bool:
        return bpy.context.scene.props.upload_all_files_in_root

    @staticmethod
    def reset_project_attribute_props() -> None:
        UserInterface.reset_project_value()
        UserInterface.reset_product_value()
        UserInterface.reset_product_version_value()
        UserInterface.reset_export_path()
        UserInterface.reset_blend_file_path()
        UserInterface.reset_root_directory()
        UserInterface.reset_upload_all_files_in_root()

    @staticmethod
    def is_render_engine_supported() -> bool:
        render_engine = bpy.context.scene.render.engine
        if render_engine not in utils_blender.get_supported_render_engines():
            bpy.context.window_manager.popup_menu(utils_blender.draw_render_engine_warning_popup,
                                                  title="Unsupported Render Engine",
                                                  icon=constants.ICON_BLANK)
            return False
        return True
