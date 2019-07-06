import bpy
import constants


class GRIDMARKETS_PT_preferences(bpy.types.Panel):

    bl_idname = constants.PANEL_PREFERENCES_ID_NAME
    bl_label = constants.PANEL_PREFERENCES_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_MAIN_ID_NAME

    def draw(self, context):
        layout = self.layout

        col_box = layout.column()

        # draw add-on preferences
        addon_preferences = context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences
        if addon_preferences is not None:
            draw = getattr(addon_preferences, "draw", None)
            if draw is not None:
                addon_preferences_class = type(addon_preferences)
                box_prefs = col_box.box()
                box_prefs.label(text="Preferences:")
                addon_preferences_class.layout = box_prefs
                try:
                    draw(context)
                except:
                    import traceback
                    traceback.print_exc()
                    box_prefs.label(text="Error (see console)", icon='ERROR')
                del addon_preferences_class.layout

        row = layout.row()
        row.operator_context = 'EXEC_AREA'

        row.scale_x = 1.3
        row.scale_y = 1.3

        row.operator("wm.save_userpref", text="Save Credentials")


classes = (
    GRIDMARKETS_PT_preferences,
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
