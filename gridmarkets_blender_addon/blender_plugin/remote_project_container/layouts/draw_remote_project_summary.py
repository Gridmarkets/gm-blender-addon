def draw_remote_project_summary(layout, project_name, project_type,
                                blender_version, project_file, blender_280_engine, blender_279_engine,
                                vray_version, remap_file):

    import bpy
    from gridmarkets_blender_addon import api_constants

    box = layout.box()
    split = box.split(factor=0.25)

    col1 = split.column()
    col2 = split.column()

    col1.label(text="Project Name:")
    col2.label(text=project_name)

    col1.label(text="Project Type:")
    col2.label(text=project_type)

    if project_type == api_constants.PRODUCTS.BLENDER:

        col1.label(text="Version")
        col2.label(text=blender_version)

        col1.label(text="Project File:")
        col2.label(text=project_name + '/' + project_file)

        if bpy.app.version[1] >= 80:
            col1.label(text="Engine")
            col2.label(text=blender_280_engine)
        elif bpy.app.version[1] <= 79:
            col1.label(text="Engine")
            col2.label(text=blender_279_engine)

    elif project_type == api_constants.PRODUCTS.VRAY:

        col1.label(text="Version")
        col2.label(text=vray_version)

        col1.label(text="Project File:")
        col2.label(text=project_name + '/' + project_file)

        col1.label(text="Re-map file")
        col2.label(text=project_name + '/' + remap_file)
