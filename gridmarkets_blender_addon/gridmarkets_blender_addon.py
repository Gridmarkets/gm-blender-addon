import os
import bpy
import pathlib

import constants
import properties
import utils
from property_sanitizer import PropertySanitizer

from .lib.gridmarkets.envoy_client import EnvoyClient
from .lib.gridmarkets.project import Project
from .lib.gridmarkets.job import Job
from .lib.gridmarkets.watch_file import WatchFile
from .lib.gridmarkets.errors import *

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

        # get the add-on preferences
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        # validate the add-on preferences
        if not self.validate_credentials(self, addon_prefs.auth_email, addon_prefs.auth_accessKey):
            return {'FINISHED'}

        try:
            # create an instance of Envoy client
            client = EnvoyClient(email = addon_prefs.auth_email, access_key = addon_prefs.auth_accessKey)

            # create a project
            # project files root folder path
            project_path = bpy.path.abspath("//")

            # name of project is optional, if not passed inferred from project root folder
            project_name = props.project_name

            # download output results to local path
            # this is optional to be passed, if not passed, by default results will get downloaded under `gm_results`
            # folder under project files path
            results_download_path = props.output_path

            # WARNING project constructor does not yet support custom output path
            project = Project(project_path, project_name)

            # get the name of the blender file
            blender_file = bpy.path.basename(bpy.context.blend_data.filepath)

            # check if the scene has been saved
            if not isinstance(blender_file, str) or len(blender_file) <= 0:
                self.report({'WARNING'}, ".blend file must be saved first.")
                return {'FINISHED'}

            # if project name is empty the project will be named after the .blend file
            project_name = project.name

            pack_location = pathlib.Path(project_path) / \
                            pathlib.Path(constants.TEMP_FILES_FOLDER) / \
                            pathlib.Path(project_name)

            packed_file_location = pack_location / pathlib.Path(blender_file)
            relative_packed_file_location = packed_file_location.relative_to(pathlib.Path(project_path))

            # create packed file
            utils.pack_blend_file(bpy.context.blend_data.filepath, str(pack_location))

            # add files to project
            # only files and folders within the project path can be added, use relative or full path
            # any other paths passed will be ignored
            project.add_folders(pack_location)

            # add the main project file (which doesnt get uploaded when using add_folders for some reason)
            project.add_files(str(pack_location / blender_file))

            JOB_NAME = PropertySanitizer.getJobName(props)
            PRODUCT_TYPE = 'blender'
            PRODUCT_VERSION = '2.80'
            OPERATION = 'render'
            RENDER_FILE = str(pathlib.Path(project_name) / relative_packed_file_location)# note the path is relative to the project name
            FRAMES = PropertySanitizer.getFrameRange(scene, props)
            OUTPUT_PREFIX = PropertySanitizer.getOutputPrefix(props)
            OUTPUT_FORMAT = scene.render.image_settings.file_format
            RENDER_ENGINE = scene.render.engine

            job = Job(
                JOB_NAME,
                PRODUCT_TYPE,
                PRODUCT_VERSION,
                OPERATION,
                RENDER_FILE,
                frames = FRAMES,
                output_prefix = OUTPUT_PREFIX,
                output_format = OUTPUT_FORMAT,
                engine = RENDER_ENGINE
            )

            # add job to project
            #project.add_jobs(job)

            # submit project
            resp = client.submit_project(project) # returns project name
            print("Response:")
            print(resp)

        except AuthenticationError as e:
            self.report({'ERROR'}, "Authentication Error: " + e.user_message)
        except InsufficientCreditsError as e:
            self.report({'ERROR'}, "Insufficient Credits Error: " + e.user_message)
        except InvalidRequestError as e:
            self.report({'ERROR'}, "Invalid Request Error: " + e.user_message)
        except APIError as e:
            self.report({'ERROR'}, "API Error: " + e.user_message)
        
        return {'FINISHED'}


    @staticmethod
    def validate_credentials(self, auth_email, auth_accessKey):
        hasEmail = False
        hasKey = False

        helpString = "\nEnter your Gridmarkets credentials by going to: Edit -> Preferences -> Add-ons -> Gridmarkets " \
                     "Blender Add-on -> preferences"

        # check an email address has been entered
        if isinstance(auth_email, str) and len(auth_email) > 0:
            hasEmail = True

        # check a auth key has been entered
        if isinstance(auth_accessKey, str) and len(auth_accessKey) > 0:
            hasKey = True

        if (not hasEmail and not hasKey):
            self.report({'ERROR_INVALID_INPUT'}, "No Gridmarkets email address or access key provided." + helpString)
            return False

        if (not hasEmail):
            self.report({'ERROR_INVALID_INPUT'}, "No Gridmarketes email address provided." + helpString)
            return False

        if (not hasKey):
            self.report({'ERROR_INVALID_INPUT'}, "No Gridmarketes access key provided." + helpString)
            return False

        return True
    
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