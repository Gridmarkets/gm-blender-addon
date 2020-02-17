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

import bpy

from gridmarkets_blender_addon.operators.base_operator import BaseOperator
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

from gridmarkets_blender_addon.meta_plugin.user import User
from gridmarkets_blender_addon.meta_plugin.errors.invalid_email_error import InvalidEmailError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_access_key_error import InvalidAccessKeyError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_user_error import InvalidUserError
from gridmarkets_blender_addon.meta_plugin.errors.api_client_error import APIClientError


def add_default_job_preset():
    from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    job_presets = plugin.get_preferences_container().get_job_preset_container().get_all()

    # do not add if there is already a preset with that name
    for job_preset in job_presets:
        if job_preset.get_name() == constants.DEFAULT_JOB_PRESET_NAME:
            return

    def add_default_job_preset(job_definition_id: str, name: str):
        job_preset_container = plugin.get_preferences_container().get_job_preset_container()

        # do not add if already added
        job_presets = job_preset_container.get_all()
        for job_preset in job_presets:
            if job_preset.get_id() == id:
                return

        job_definitions = plugin.get_api_client().get_cached_api_schema().get_job_definitions()
        for job_definition in job_definitions:
            if job_definition.get_definition_id() == job_definition_id:
                job_preset_container.append(JobPreset(name, job_definition, is_locked=True))

    # add default job presets
    add_default_job_preset(api_constants.JOB_DEFINITION_IDS.BLENDER_2_8X_CYCLES, constants.DEFAULT_JOB_PRESET_NAME)



class GRIDMARKETS_OT_sign_in_new_user(BaseOperator):
    bl_idname = "gridmarkets.sign_in_new_user"
    bl_label = "Sign-in new user"
    bl_options = {"REGISTER"}
    bl_description = "Sign in " + constants.COMPANY_NAME

    def handle_expected_result(self, result: any) -> bool:
        user_interface = self.get_plugin().get_user_interface()

        if result is None:
            user_interface.set_auth_email_validity_flag(True)
            user_interface.set_auth_access_key_validity_flag(True)
            user_interface.set_auth_email_validity_message("")
            user_interface.set_auth_access_key_validity_message("")
            user_interface.set_user_validity_flag(True)
            user_interface.set_user_validity_message("")
            user_interface.set_layout(constants.SUBMISSION_SETTINGS_VALUE)
            return True

        elif type(result) == InvalidEmailError:
            user_interface.set_auth_email_validity_flag(False)
            user_interface.set_auth_access_key_validity_flag(True)
            user_interface.set_auth_email_validity_message(result.user_message)
            user_interface.set_auth_access_key_validity_message("")
            return True

        elif type(result) == InvalidAccessKeyError:
            user_interface.set_auth_email_validity_flag(True)
            user_interface.set_auth_access_key_validity_flag(False)
            user_interface.set_auth_email_validity_message("")
            user_interface.set_auth_access_key_validity_message(result.user_message)
            return True

        elif type(result) == InvalidUserError:
            user_interface.set_auth_email_validity_flag(True)
            user_interface.set_auth_access_key_validity_flag(True)
            user_interface.set_user_validity_flag(False)
            user_interface.set_user_validity_message(result.user_message)
            return True

        elif type(result) == APIClientError:
            user_interface.set_auth_email_validity_flag(True)
            user_interface.set_auth_access_key_validity_flag(True)
            user_interface.set_user_validity_flag(False)
            user_interface.set_user_validity_message(result.user_message)
            return True

        return False

    def execute(self, context: bpy.types.Context):
        self.setup_operator()

        plugin = self.get_plugin()
        api_client = plugin.get_api_client()

        user_interface = plugin.get_user_interface()
        auth_email = user_interface.get_auth_email()
        auth_access_key = user_interface.get_auth_access_key()
        user = User(auth_email, auth_access_key)

        def sign_in(user, skip_validation=False):
            result = api_client.sign_in(user, skip_validation=skip_validation)
            add_default_job_preset()
            return result

        ################################################################################################################

        method = sign_in

        args = (
            user,
        )

        kwargs = {
            "skip_validation": False,
        }

        running_operation_message = "Signing in..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)


classes = (
    GRIDMARKETS_OT_sign_in_new_user,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)
