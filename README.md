# GridMarkets Blender Add-on
A Blender add-on for uploading Blender Projects to GridMarkets and for specifying render jobs.

- [Installing the Add-on](#installing-the-add-on)
  - [Installing the Add-on Via Envoy](#installing-the-add-on-via-envoy)
  - [Installing the Add-on Manually](#installing-the-add-on-manually)
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
  - [Submitting a Job](#submitting-a-job)
    - [Submit and upload at the same time](#submit-and-upload-at-the-same-time)
    - [Resubmit a job without reuploading](#resubmit-a-job-without-reuploading)
  - [Uploading Projects without Submitting](#uploading-projects-without-submitting)
  - [Importing Existing Projects](#importing-existing-projects)
  - [Job Presets](#job-presets)
  - [Submitting a V-Ray Scene](#submitting-a-v-ray-scene)

![image showing a preview of the add-on](static/floating_window.png)

## Installing the Add-on
### Installing the Add-on Via Envoy
The recommended way to install the add-on is through GridMarkets Envoy. For instructions on how to install via Envoy 
see: https://support.gridmarkets.com/portal/en/kb/articles/installing-plug-ins-via-envoy

### Installing the Add-on Manually
The add-on can also be installed manually. Either clone this repo and build a zip or ask support for a link to the 
latest build. Then install  

When installing manually you must create a config.ini file within the gridmarkets_blender_addon folder that the add-on
is installed to containing the paths to the python ee you would like to use and submit2gm.

The default paths used when installing via Envoy on Windows are the following:
```
[default]
ENVOY_PYTHON_PATH: C:/Users/<user>/AppData/Local/Programs/GridMarkets/gm-tools-windows/pythonw.exe
SUBMIT2GM_PATH: C:/Users/<user>/AppData/Roaming/GridMarkets/plugins/submit2gm/submit2gm.pyw
```

To install the add-on you must first either download one of the pre-built zip files or follow the below instructions for
how to build the add-on from source.

### Building from Sources

#### Installing Dependencies
The add-on depends on the GridMarkets api library and blender-asset-tracer (BAT). Use `python setup.py wheels` to 
install the wheel dependencies to the `gridmarkets_blender_addon/lib` directory. Dependencies **must** be installed 
before using `bzip` or `fdist` as these will not currently check to make sure libraries are downloaded.

The add-on also interfaces with GridMarkets Submit2gm and Envoy clients which you will have to install separately.

#### Building .Zip File
To build the add-on as a .zip file that can be imported into blender run `python ./setup.py bzip`. The .zip will be 
output to the `./dist` directory by default or you can use the `-d` argument to pass a custom path. For example
`python .\setup.py bzip -d ./custom_path/zip_name`.

### Installing the Zipped Add-on
You can then import the built .zip file into Blender by going to `edit -> preferences -> Add-ons -> install`. Activate the 
add-on by searching `GridMarkets blender addon` and ticking it's checkbox.

>
>Note: If you already have the GridMarkets Blender add-on installed and want to update to a newer version it is best to 
**uninstall the previous version and then restart blender** before installing the new version. Otherwise you may 
encounter errors.

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

After clicking the button the GridMarkets Submit2gm client should open, sign-in (if not already signed in) and display
the submission UI.
