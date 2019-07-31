class PanelOverloader():
    """
    A class which takes a blender panel and replaces it's draw method with conditonal draw method which will use either
    the original draw method or a new draw method depending on some condition. If the condition is true then the new
    draw method is used.
    """

    @staticmethod
    def _default_overload_condition():
        return True

    def __init__(self, panel, draw_method, overload_condition = _default_overload_condition):
        self._panel = panel
        self._base_draw_method = panel.draw

        PanelOverloader._overload_panel(panel, draw_method, overload_condition, panel.draw)

    @staticmethod
    def _overload_panel(panel, draw_method, overload_condition, base_draw_method):
        """ Sets the panel's draw method to use our new draw method"""

        def _draw(self, context):
            # if the overload condition is met
            if overload_condition(self, context):
                # use the new draw method
                draw_method(self, context)
            else:
                # otherwise use the original draw method for the panel
                base_draw_method(self, context)

        panel.draw = _draw

    def reset_panel(self):
        """ Resets the panel's draw method back to it's original draw method """
        self._panel.draw = self._base_draw_method
        return None
