import bpy


class GRIDMARKETS_OT_remove_unused_screens(bpy.types.Operator):
    bl_idname = "gridmarkets.delete_unused_screens"
    bl_label = "Delete unused screens"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        screen_items = list(map(lambda t: t[1], bpy.data.screens.items()))
        print()
        print("screen items")
        for screen_item in screen_items:
            print("name: ", screen_item.name)

        unused_screens = []
        for screen_item in screen_items:
            if screen_item.name.startswith("GRIDMARKETS_INJECTION_SCREEN"):
                unused_screens.append(screen_item)

        print()
        print("unused screens")
        for screen_item in unused_screens:
            print(screen_item.name)

        if screen_item in unused_screens:
            #bpy.ops.screen.delete({'screen': screen_item})


            """
            screen_to_delete = screen_item.name

            current_screen = bpy.context.window.screen.name
            delete = screen_to_delete
            bpy.ops.screen.delete({'screen': bpy.data.screens[delete]})
            bpy.context.window.screen = bpy.data.screens[current_screen]
            """

        #bpy.ops.screen.screen_set(delta=1)
        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_remove_unused_screens,
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
