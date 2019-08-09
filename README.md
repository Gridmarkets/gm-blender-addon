# GridMarkets Blender Add-on
A Blender add-on for uploading Blender Projects to GridMarkets and for specifying render jobs.

- [Installing the Add-on](#installing-the-add-on)
  - [Pre-built Files](#pre-built-files)
  - [Building from Sources](#building-from-sources)
    - [Installing Dependencies](#installing-dependencies)
    - [Building .Zip File](#building-zip-file)
  - [Installing the Zipped Add-on](#installing-the-zipped-add-on)
  - [Implicit Installation for Development](#implicit-installation-for-development)
    - [Custom Scripts Path](#custom-scripts-path)
  - [Reloading Add-ons](#reloading-add-ons)
- [Using the Add-on](#using-the-add-on)
  - [Authentication](#authentication)
  - [Submitting a Project](#submitting-a-project)

![image showing a preview of the add-on](static/floating_window.png)

## Installing the Add-on

To install the add-on you must first either download one of the pre-built zip files or follow the below instructions for
how to build the add-on from source.

### Pre-built Files

| Blender Version   | Add-on Download Link|
|-------------------|--------|
| 2.80  | [gridmarkets_blender_addon_2_80_v1_0_0.zip](https://gridmarkets-misc.s3-ap-southeast-1.amazonaws.com/gridmarkets_blender_addon_v2_80_1_0_0.zip)  |
| 2.79  | [gridmarkets_blender_addon_2_79_v1_0_0.zip](https://gridmarkets-misc.s3-ap-southeast-1.amazonaws.com/gridmarkets_blender_addon_v2_79_1_0_0.zip)  |

### Building from Sources

#### Installing Dependencies
The add-on depends on the GridMarkets api library and blender-asset-tracer (BAT). Use `python setup.py wheels` to 
install the wheel dependencies to the `gridmarkets_blender_addon/lib` directory. Dependencies **must** be installed 
before using `bzip` or `fdist` as these will not currently check to make sure libraries are downloaded.

#### Building .Zip File
To build the add-on as a .zip file that can be imported into blender run `python ./setup.py bzip`. The .zip will be 
output to the `./dist` directory by default or you can use the `-d` argument to pass a custom path. For example
`python .\setup.py bzip -d ./custom_path/zip_name`.

### Installing the Zipped Add-on
You can then import the built .zip file into Blender by going to `edit -> preferences -> Add-ons -> install`. Activate the 
add-on by searching `GridMarkets blender addon` and ticking it's checkbox.

![gif showing how to install add-ons inside Blender](static/blender_addon_install_walkthrough.gif)

### Implicit Installation for Development
To save having to repack the add-on as a .zip and installing it into blender after each change you can either use 
`python .\setup.py fdist -d "path\to\blender addons\"` to directly install the add-on into blender (it will replace any 
existing add-ons of the same name) or you can setup Blender with a custom add-ons path to load the add-on directly from
the source files.

#### Custom Scripts Path
Setting up a custom scripts path is done by editing `edit -> prefereces -> File Paths -> Scripts` to point to a custom 
directory. This directory must be setup to mirror the structure of Blender's default scripts folder. This means it must 
contain an `addons` sub-directory which blender will use when searching for custom add-ons. You can then create a 
symlink to the location of the `gm-blender-addon\gridmarkets_blender_addon` folder. See 
https://docs.blender.org/manual/en/dev/preferences/file_paths.html#scripts-path for more information about using a 
custom scripts path.

For an example setup, in Windows create a folder called `C:\blender-addons` and set Blender's `Scripts` path to it (as 
described above). Then create a sub-directory called `addons` under the first folder. Create a symbolic link to the 
add-on using `mklink /D C:\blender-addons\addons\gridmarkets_blender_addon 
C:\<path to repo>\gm-blender-addon\gridmarkets_blender_addon` (using cmd not PowerShell). Now you should be able to 
activate the add-on within Blender, and reload any changes to the source without packing as a zip and re-installing.

#### Reloading Add-ons
To reload the add-on after making a change to the
add-on's source code use `F3` (or `Cmd + F` on MacOs) in Blender to open up the search window and search for 
`Reload Scripts`. This will reload the add-on.

![image showing how to reload scripts inside Blender](static/reload_scripts.png)

## Using the Add-on
The add-on window can be opened by pressing the 'Open GridMarkets add-on' button in the top bar.

![image showing how to open the add-on](static/open_button.png)

The add-on depends on GridMarkets' Envoy being installed and running in order to work.

### Authentication
You must provide your GridMarkets email and access key (__not your password__) before you can upload or submit and 
projects. You can do this under the __Credentials__ tab or under the add-on preferences section for the add-on. 

![image showing where to insert email and access key](static/add-on_preferences.png)

For Blender to remember a users credentials between sessions they must click the `Save Preferences` button also shown in 
the above image.

### Submitting a Project

Once opened you have the option of submitting your current scene using blender's render settings in an easy one click
submit process. There is no requirement to save the .blend file before submitting, the add-on will automatically save a 
copy of the currently open scene to a temporary directory. It will then create a packed version of the same file using 
BAT and upload via the API. The temporary packed files will be deleted after they are uploaded.

![GIF showing the submission settings tab](static/submission_view.gif)

You can also can define custom jobs that override blender's render and output settings to give you more control in the 
__Job Presets__ tab. 

![image showing the job presets tab](static/job_presets_view.png)

Or you can upload projects in the __Projects__ tab and run jobs against them later.

![image showing the projects tab](static/projects_view.png)


