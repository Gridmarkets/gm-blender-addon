# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2019  GridMarkets
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import typing
from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher


def register_menus(self):
    from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute
    from gridmarkets_blender_addon.meta_plugin.transition import Transition
    from gridmarkets_blender_addon.meta_plugin.attribute_type import AttributeType
    from gridmarkets_blender_addon.meta_plugin.attribute import EnumItem, EnumAttribute
    from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants

    plugin = PluginFetcher.get_plugin()
    api_schema = plugin.get_api_client().get_api_schema()

    # get the project attribute that specifies the name
    projects = api_schema.get_product_project_attribute()


    def register_menus_recursive(attribute: ProjectAttribute):

        if attribute.get_type() == AttributeType.ENUM.value:
            items: typing.List[EnumItem] = attribute.get_items()
            transitions: typing.List[Transition] = attribute.get_transitions()

            mappings: typing.List[(EnumItem, Transition)] = []

            for item in items:
                for transition in transitions:
                    if item.get_key() == transition.get_transition_formula():
                        mappings.append((item, transition))

            # get transitions to job definitions
            job_definition_mappings = []

            for mapping in mappings:
                pass
                # mapping[1]

        children = attribute.get_children()

        sub_menus: typing.List[bpy.types.Menu] = []

        def draw_menus(self, context):
            layout = self.layout

            for menu in self._menus:
                layout.menu(menu.bl_idname)

        menu = type("ProjectAttributeMenu",
                                  (bpy.types.Menu),
                                  {
                                      "bl_idname": "GRIDMARKETS_MT_" + ProjectAttribute.get_id(),
                                      "bl_label": ProjectAttribute.get_display_name(),
                                      "bl_description": ProjectAttribute.get_description(),
                                      "_menus": sub_menus,
                                      "draw": draw_menus
                                  })

        #from bpy.utils import register_class
        #register_class(menu)

        return menu


    # register a menu for all the products

    # register a menu for each of the product versions



    """
    get all job definitions
    
    create an operator for each job definition
    
    
    get enum project attribute
    for each enum item find the cooresponding translation
    
    for each enum item with a transition recurse down its tree until the next enum attribute is found
    
    
    if attribute is a valid project add draw all job definition operators linked to it
    

    """







classes = ()


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
