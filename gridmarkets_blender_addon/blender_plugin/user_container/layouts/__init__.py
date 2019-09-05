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

def draw_user_profiles_list(self, context):
    import bpy
    from gridmarkets_blender_addon import constants, utils_blender
    from gridmarkets_blender_addon.blender_plugin.user.list_items.user_list import GRIDMARKETS_UL_user
    from gridmarkets_blender_addon.blender_plugin.user_container.operators.delete_focused_profile import \
        GRIDMARKETS_OT_delete_focused_profile
    from gridmarkets_blender_addon.blender_plugin.user_container.operators.load_focused_profile import \
        GRIDMARKETS_OT_load_focused_profile
    from gridmarkets_blender_addon.blender_plugin.user_container.operators.set_focused_profile_as_default import \
        GRIDMARKETS_OT_set_focused_profile_as_default

    layout = self.layout
    addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

    user_profiles_box = layout.box()
    user_profiles_box.alignment = "CENTER"
    user_profiles_box.label(text="Saved User Profiles:")

    sub = user_profiles_box.row()
    sub.alignment="LEFT"
    sub.enabled = False
    sub.label(text="A list of stored " + constants.COMPANY_NAME + "' profiles for easy access.")

    row = user_profiles_box.row()

    col1 = row.column()
    col1.template_list(GRIDMARKETS_UL_user.bl_idname, "",
                       addon_prefs.saved_profiles, "user_profiles",
                       addon_prefs.saved_profiles, "focused_user",
                       rows=3, sort_lock=True)
    col1.operator(GRIDMARKETS_OT_load_focused_profile.bl_idname, text="Load Credentials")

    col2 = row.column()

    col2.operator(GRIDMARKETS_OT_delete_focused_profile.bl_idname, text="", icon=constants.ICON_REMOVE)
    col2.operator(GRIDMARKETS_OT_set_focused_profile_as_default.bl_idname, text="", icon=constants.ICON_DEFAULT_USER)


def draw_sign_in_form(self, context):
    from gridmarkets_blender_addon import constants, utils_blender
    from gridmarkets_blender_addon.icon_loader import IconLoader

    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.blender_plugin.user_container.operators.sign_in import GRIDMARKETS_OT_sign_in_new_user

    layout = self.layout
    scene = context.scene
    props = scene.props

    # get the company icon
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
    iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

    plugin = PluginFetcher.get_plugin()
    user_interface = plugin.get_user_interface()
    user_container = plugin.get_preferences_container().get_user_container()

    def _draw_register(layout):
        row = layout.row()
        row.alignment = "CENTER"
        row.emboss = "PULLDOWN_MENU"

        row.label(text="Don't have an account yet?")
        row.operator(
            constants.OPERATOR_OPEN_REGISTER_ACCOUNT_LINK_ID_NAME,
            text="Register Here"
        )

    def _draw_string_input_field(layout, label: str, source, prop_name: str, is_valid: bool, validation_msg: str,
                                 enabled: bool):
        field_layout = layout.split(factor=0.2)
        field_layout.alignment = "CENTER"
        field_layout.enabled = enabled
        col1 = field_layout.column()
        col1.alignment = "LEFT"
        col1.label(text=label)

        col2 = field_layout.column()
        col2.alignment = "RIGHT"
        col2.alert = not is_valid
        col2.prop(source, prop_name, text="")

        if col2.alert and validation_msg is not None and len(validation_msg) > 0:
            alert = col2.row()
            alert.alignment = "RIGHT"
            alert.scale_x = 0.5
            alert.label(text=validation_msg)

    box = layout.box()

    row = box.row()
    row.alignment = "CENTER"
    row.scale_x = 2

    signin_box = row.box()
    signin_box.label(text=constants.COMPANY_NAME + " Sign-in:", icon_value=iconGM.icon_id)

    _draw_string_input_field(signin_box,
                             "Email:",
                             props.user_interface,
                             "auth_email_input",
                             user_interface.get_auth_email_validity_flag(),
                             user_interface.get_auth_email_validity_message(),
                             not user_interface.get_signing_in_flag())

    _draw_string_input_field(signin_box,
                             "Access key:",
                             props.user_interface,
                             "auth_access_key_input",
                             user_interface.get_auth_access_key_validity_flag(),
                             user_interface.get_auth_access_key_validity_message(),
                             not user_interface.get_signing_in_flag())

    sign_in_button = signin_box.row()
    sign_in_button.scale_y = 1.3
    if user_interface.get_signing_in_flag():
        sign_in_button.enabled = False
        sign_in_button.operator(
            GRIDMARKETS_OT_sign_in_new_user.bl_idname,
            text="Signing in...",
            icon_value=utils_blender.get_spinner(user_interface.get_signing_in_spinner()).icon_id
        )
    elif user_interface.get_user_validity_flag():
        sign_in_button.operator(
            GRIDMARKETS_OT_sign_in_new_user.bl_idname,
            text="Sign-in"
        )

        if not (user_interface.get_auth_email_validity_flag() and
                user_interface.get_auth_access_key_validity_flag()):
            sign_in_button.enabled = False

    else:
        sign_in_button.alert = True
        sign_in_button.operator(
            GRIDMARKETS_OT_sign_in_new_user.bl_idname,
            text=user_interface.get_user_validity_message(),
            icon=constants.ICON_ERROR
        )

    signin_box.separator()
    register_layout = signin_box.row()
    register_layout.scale_x = 0.5
    _draw_register(register_layout)

    if user_container.size():
        from types import SimpleNamespace
        user_profiles_layout = row.row()
        user_profiles_layout.scale_x = 0.5
        draw_user_profiles_list(SimpleNamespace(layout=user_profiles_layout), context)

def draw_user_container(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    api_client = plugin.get_api_client()
    user_container = plugin.get_preferences_container().get_user_container()

    if api_client.is_user_signed_in():
        from gridmarkets_blender_addon.blender_plugin.user_container.operators.sign_out import GRIDMARKETS_OT_sign_out
        from gridmarkets_blender_addon import constants
        from gridmarkets_blender_addon.icon_loader import IconLoader

        layout = self.layout

        # get the company icon
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

        box = layout.box()
        box.scale_x = 2
        row = box.row()
        row.alignment = "CENTER"

        sign_out_box = row.box()
        sign_out_box.alignment="CENTER"

        sign_out_box.label(text=constants.COMPANY_NAME + " Sign-out:", icon_value=iconGM.icon_id)

        row = sign_out_box.row()
        row.alignment = "CENTER"
        row.scale_x = 0.5
        row.emboss = "NONE"

        # use an operator so that it is actually centered
        row.operator(GRIDMARKETS_OT_sign_out.bl_idname, text="Signed in as: " + api_client.get_signed_in_user().get_auth_email())

        row = sign_out_box.row()
        row.operator(GRIDMARKETS_OT_sign_out.bl_idname)

    else:
        draw_sign_in_form(self, context)
