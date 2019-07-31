import constants


def draw_console(self, context):
    layout = self.layout
    props = context.scene.props
    box = layout.box()
    box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=6, sort_lock=True)
    box.operator(constants.OPERATOR_COPY_LOGS_TO_CLIPBOARD_ID_NAME)


def draw_compact_console(self, context):
    layout = self.layout
    props = context.scene.props
    box = layout.box()
    box.alignment = "RIGHT"
    box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=4, sort_lock=True)
