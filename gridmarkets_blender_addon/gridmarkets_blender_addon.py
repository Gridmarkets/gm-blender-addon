import os
import bpy
import pathlib

import constants
import properties
import utils

from temp_directory_manager import TempDirectoryManager
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
temp_dir_manager = TempDirectoryManager()

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------


class GRIDMARKETS_OT_Submit(bpy.types.Operator):
    """Class to represent the 'Render' operation. Currently only uploads the project file to the servers."""
    
    bl_idname = "gridmarkets.render"
    bl_label = "Submit"

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

            blend_file_name = None
            project_name = None

            # if the file has been saved
            if bpy.context.blend_data.is_saved:
                # use the name of the saved .blend file
                blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)
                project_name = PropertySanitizer.getProjectName(props, default_project_name=blend_file_name)
            else:
                # otherwise create a name for the packed .blend file
                blend_file_name = 'main_GM_blend_file_packed.blend'
                project_name = PropertySanitizer.getProjectName(props)

                # warn user that the file is not saved
                self.report({'WARNING'}, "The current blender scene has not been saved. The scene will submit but any "
                                         "render files will not automatically download.")

            # create a new temp directory
            temp_dir_path = temp_dir_manager.get_temp_directory()

            blend_file_path = temp_dir_path / blend_file_name

            # save a copy of the current scene to the temp directory. This is so that if the file has not been saved
            # or if it has been modified since it's last save then the submitted .blend file will represent the
            # current state of the scene
            bpy.ops.wm.save_as_mainfile(copy=True, filepath=str(blend_file_path), relative_remap=True,
                                        compress=True)

            # create directory to contain packed project
            packed_dir = temp_dir_path / project_name
            os.mkdir(str(packed_dir))

            # pack the .blend file to the pack directory
            utils.pack_blend_file(str(blend_file_path), str(packed_dir))

            # delete pack-info.txt if it exists
            pack_info_file = pathlib.Path(packed_dir / 'pack-info.txt')
            if pack_info_file.is_file():
                pack_info_file.unlink()

            # create the project
            project = Project(str(packed_dir), project_name)

            # associate this project with the temp directory so the temp directory can be removed once the project is
            # complete
            temp_dir_manager.associate_project(temp_dir_path, project)

            # add files to project
            # only files and folders within the project path can be added, use relative or full path
            # any other paths passed will be ignored
            project.add_folders(str(packed_dir))

            if bpy.context.blend_data.is_saved:
                # add watch file
                output_pattern = '{0}/.+'.format(project.remote_output_folder)

                # download path
                download_path = str(pathlib.Path(bpy.context.blend_data.filepath).parent / 'gm_results')

                # create a watch file
                watch_file = WatchFile(output_pattern, download_path)

                # add watch files, this will auto download results to the defined `download_path`
                project.add_watch_files(watch_file)

            JOB_NAME = PropertySanitizer.getJobName(props)
            PRODUCT_TYPE = 'blender'
            PRODUCT_VERSION = '2.80'
            OPERATION = 'render'
            # note the path is relative to the project name
            RENDER_FILE = str(pathlib.Path(project_name) / blend_file_name).replace('\\', '/')
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
                frames=FRAMES,
                output_prefix=OUTPUT_PREFIX,
                output_format=OUTPUT_FORMAT,
                engine=RENDER_ENGINE
            )

            # add job to project
            project.add_jobs(job)

            # submit project
            resp = client.submit_project(project)  # returns project name
            print("Response:")
            print(resp)

        except AuthenticationError as e:
            self.report({'ERROR'}, "Authentication Error: " + e.user_message)
        except InsufficientCreditsError as e:
            self.report({'ERROR'}, "Insufficient Credits Error: " + e.user_message)
        except InvalidRequestError as e:
            self.report({'ERROR'}, "Invalid Request Error: " + e.user_message)
        except APIError as e:
            self.report({'ERROR'}, "API Error: " + str(e.user_message))

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
        
        # 'Submit' button
        row = layout.row(align=True)
        row.operator(GRIDMARKETS_OT_Submit.bl_idname)
        
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
    GRIDMARKETS_OT_Submit,
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
