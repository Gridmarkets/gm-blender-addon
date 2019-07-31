import constants


def draw_sidebar(self, context):
    layout = self.layout
    props = context.scene.props

    layout.label(text="Links")

    col = layout.column()
    col.scale_x = 1
    col.scale_y = 2

    # Portal manager link
    col.operator(constants.OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME, icon=constants.ICON_URL)

    # Cost calculator
    col.operator(constants.OPERATOR_OPEN_COST_CALCULATOR_ID_NAME, icon=constants.ICON_URL)
    col.operator(constants.OPERATOR_OPEN_PREFERENCES_ID_NAME, icon=constants.ICON_PREFERENCES, text="Preferences")
    col.operator(constants.OPERATOR_OPEN_HELP_URL_ID_NAME, icon=constants.ICON_HELP)
