# the addons package name
ADDON_PACKAGE_NAME = "GridmarketsBlenderAddon"

# the icons folder contains custom icons for the UI
ICONS_FOLDER = "icons"

# the name of the gridmarkets logo file
LOGO_ICON_FILE_NAME = "logo.png"

# the url of the render manager
RENDER_MANAGER_URL = "https://portal.gridmarkets.com/init/member_plugin/index"

# (not used since api does not yet support output paths)
DEFAULT_OUTPUT_PATH = "/gm_results"

# plugin versioning
PLUGIN_VERSION = { "major": 0, "minor": 3, "build" : 2}



# register module
def register():
    pass

# unregister module
def unregister():
    pass

if __name__ == "__main__":
    register()