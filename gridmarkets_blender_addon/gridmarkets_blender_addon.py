import os
import bpy

import constants
import properties

from gridmarkets import EnvoyClient, Project, Job, WatchFile

# ------------------------------------------------------------------------
#    Global Variables
# ------------------------------------------------------------------------

# Used to store any previews for images (In this case the Gridmarkets custom icon)
preview_collections = {}

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
class GRIDMARKETS_OT_Render(bpy.types.Operator):
    """Class to represent the 'Render' operation. Currently only uploads the project file to the servers."""
    
    bl_idname = "gridmarkets.render"
    bl_label = "Render"

    def execute(self, context):
        scene = context.scene
        props = scene.props
        
        # create an instance of Envoy client
        client = EnvoyClient(email = props.auth_email, access_key = props.auth_key)
        
        # create a project
        # project files root folder path
        project_path = bpy.path.abspath("//")

        # name of project is optional, if not passed inferred from project root folder
        project_name = props.project_name

        # download output results to local path
        # this is optional to be passed, if not passed, by default results will get downloaded under `gm_results` folder under project files path
        results_download_path = props.output_path
    
        # WARNING project constructor does not yet support custom output path
        project = Project(project_path, project_name)
        
        # add files to project
        # only files and folders within the project path can be added, use relative or full path
        # any other paths passed will be ignored
        project.add_files(bpy.path.basename(bpy.context.blend_data.filepath))
        
        # submit project
        resp = client.submit_project(project) # returns project name
        
        print("Response:")
        print(resp)
        
        return {'FINISHED'}
    
class GRIDMARKETS_OT_Open_Manager_Portal(bpy.types.Operator):
    """Class to represent the 'Open Manager Portal' operation. Opens the portal in the users browser."""
    
    bl_idname = "gridmarkets.open_portal"
    bl_label = "Open Manager Portal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # open the render manager url in the users browser
        bpy.ops.wm.url_open(url=constants.RENDER_MANAGER_URL)
        return {"FINISHED"}

# ------------------------------------------------------------------------
#    Panels
# ------------------------------------------------------------------------

class GRIDMARKETS_PT_Main(bpy.types.Panel):
    """Class to represent the plugins main panel. Contains all sub panels as well as 'Render' and 'Open Manager Portal' buttons."""
    
    bl_idname = "gridmarkets_main_panel"
    bl_label = "GridMarkets"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    @classmethod
    def poll(self,context):
        return True #context.object is not None

    def draw(self, context):
        layout = self.layout
        
        # get the Gridmarkets icon
        pcoll = preview_collections["main"]
        iconGM = pcoll["my_icon"]
        
        # get the plugin version as a string
        versionStr = 'Gridmarkets v' + str(constants.PLUGIN_VERSION['major']) + '.' + str(constants.PLUGIN_VERSION['minor']) + '.' + str(constants.PLUGIN_VERSION['build'])
        
        # display Gridmarkets icon and version
        layout.label(text=versionStr, icon_value=iconGM.icon_id)
        
        # 'Render' button
        row = layout.row(align=True)
        row.operator(GRIDMARKETS_OT_Render.bl_idname)
        
        # Portal manager link
        row = layout.row(align=True)
        row.operator(GRIDMARKETS_OT_Open_Manager_Portal.bl_idname)        


class GRIDMARKETS_PT_Job_Info(bpy.types.Panel):
    """The plugin's job info sub panel."""
    
    bl_idname = "gridmarkets_job_info_sub_panel"
    bl_label = "Job Info"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_parent_id = "gridmarkets_main_panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Create two columns, by using a split layout.
        split = layout.split(factor=0.5)
        
        # First column
        col = split.column()
        col.label(text = "Project Name:")
        col.label(text = "Submission Label:")
        col.label(text = "Artist Name:")
        col.label(text = "Submission Comment:")
        col.label(text = "Blender Version:")
        col.label(text = "Render Engine:")
        
        # Second column, aligned
        col = split.column()
        col.prop(scene.props, "project_name", text = "")
        col.prop(scene.props, "submission_label", text = "")
        col.prop(scene.props, "artist_name", text = "")
        col.prop(scene.props, "submission_comment", text = "")
        
        col.alignment = 'RIGHT'
        col.label(text=bpy.app.version_string)
        col.label(text=bpy.context.scene.render.engine)


class GRIDMARKETS_PT_Render_Settings(bpy.types.Panel):
    """The plugin's render settings sub panel."""
    
    bl_idname = "gridmarkets_render_settings_sub_panel"
    bl_label = "Render Settings"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_parent_id = "gridmarkets_main_panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.prop(scene.props, "override_project_render_settings")
        
        box = layout.box()
        box.active = scene.props.override_project_render_settings
        # Create two columns, by using a split layout.
        split = box.split()
        
        # First column
        col = split.column()
        col.label(text="Frame Start")
        col.label(text="Frame End")
        col.label(text="Step Size")

        # Second column, aligned
        col = split.column(align=True)
        col.prop(scene.props, "render_frame_start")
        col.prop(scene.props, "render_frame_end")
        col.prop(scene.props, "render_frame_step")
        
class GRIDMARKETS_PT_Output_Settings(bpy.types.Panel):
    """The plugin's output settings sub panel."""
    
    bl_idname = "gridmarkets_output_settings_sub_panel"
    bl_label = "Output Settings"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_parent_id = "gridmarkets_main_panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()
        col.prop(scene.props, "output_path")
        col.prop(scene.props, "output_prefix")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------
classes = (
    GRIDMARKETS_OT_Render,
    GRIDMARKETS_OT_Open_Manager_Portal,
    GRIDMARKETS_PT_Main,
    GRIDMARKETS_PT_Job_Info,
    GRIDMARKETS_PT_Render_Settings,
    GRIDMARKETS_PT_Output_Settings
)

def registerIcons():
    from bpy.utils import previews
    
    # register icons
    pcoll = bpy.utils.previews.new()

    # path to the folder where the icon is
    # the path is calculated relative to this py file inside the addon folder
    my_icons_dir = os.path.join(os.path.dirname(__file__), constants.ICONS_FOLDER)

    # load a preview thumbnail of the icon and store in the previews collection
    pcoll.load("my_icon", os.path.join(my_icons_dir, constants.LOGO_ICON_FILE_NAME), 'IMAGE')

    preview_collections["main"] = pcoll

def register():
    from bpy.utils import register_class
    
    # register custom icons
    registerIcons()
    
    # register classes
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    
    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)
    
    # clear the preview collections object of icons
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()