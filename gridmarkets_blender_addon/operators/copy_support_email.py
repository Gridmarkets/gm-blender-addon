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
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_copy_support_email(bpy.types.Operator):
    bl_idname = constants.OPERATOR_COPY_SUPPORT_EMAIL_ID_NAME
    bl_label = constants.OPERATOR_COPY_SUPPORT_EMAIL_LABEL

    def execute(self, context):
        def _draw(self, context):
            layout = self.layout
            layout.label(text="Reach our support team at \"" + constants.SUPPORT_EMAIL + "\".")
            layout.separator()
            layout.label(text="Our support email has been copied to your clipboard.",
                         icon=constants.ICON_COPY_TO_CLIPBOARD)

        bpy.context.window_manager.clipboard = constants.SUPPORT_EMAIL
        bpy.context.window_manager.popup_menu(_draw)
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_copy_support_email,
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
