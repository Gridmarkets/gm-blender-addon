import constants

def draw_preferences(self, context):
    layout = self.layout

    col_box = layout.column()

    # draw add-on preferences
    addon_preferences = context.user_preferences.addons[constants.ADDON_PACKAGE_NAME].preferences
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
                box_prefs.label(text="Error (see console)", icon=constants.ICON_ERROR)
            del addon_preferences_class.layout

    row = layout.row()
    row.operator_context = 'EXEC_AREA'

    row.scale_x = 1.3
    row.scale_y = 1.3

    row.operator("wm.save_userpref", text="Save Credentials")