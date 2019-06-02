# Gridmarkets Blender Add-on

A Blender add-on for uploading Blender Projects to Gridmarkets and for specifying render jobs.

## Installing the Addon

To build the add-on as a .zip file that can be imported into blender run `python ./setup.py bzip`. The .zip will be 
output to the ./dist directory by default. 

You can then import this into Blender by going `edit -> preferences -> Add-ons -> install`. Then you will be able to 
active the add-on by searching `gridmarkets blender addon` and ticking it's checkbox.

### Implicit instillation for Development
To save having to repack the add-on as a .zip and installing it into blender after each change you can either use 
`python .\setup.py fdist -d "path\to\blender addons\"` to directly install the add-on into blender (it will replace any 
existing add-ons of the same name) or you can setup blender with a custom add-ons path to load the addon directly from
the source files

### todo
- ~~Handle dependencies outside of the project root.~~
- ~~Handle linked blender files which themselves have their own dependencies.~~
- Currently the add-on re-packs and re-uploads the entire project for each render, it should detect which files have .
  been updated and act accordingly.
- Clean up temp files generated from packing the project.
- [Extension] it would be possible to render single frames in a distributed way by creating a fake animation where each
  frame is the same and then re-combining the frames client side. Very usefull for artists who are trying to create 
  still images.