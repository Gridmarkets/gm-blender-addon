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

__all__ = 'get_blender_icon_tuple_for_job_definition', 'get_blender_icon_for_job_definition'

from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition


# todo add to job definition sub class
def get_blender_icon_tuple_for_job_definition(job_definition: JobDefinition) -> (str, int):
    """ Gets the icon and icon_value values for a JobDefinition """
    from gridmarkets_blender_addon import constants, icon_loader
    from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

    product_attribute = job_definition.get_attribute_with_key(api_constants.ATTRIBUTE_NAMES.PRODUCT)

    icon = constants.ICON_NONE
    icon_value = 0

    if product_attribute:
        product = product_attribute.get_attribute().get_default_value()
        preview_collection = icon_loader.IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]

        if product == api_constants.PRODUCTS.BLENDER:
            icon = constants.ICON_BLENDER
        elif product == api_constants.PRODUCTS.VRAY:
            icon_value = preview_collection[constants.VRAY_LOGO_ID].icon_id
        elif product == api_constants.PRODUCTS.MOE:
            icon_value = preview_collection[constants.MOE_LOGO_ID].icon_id
        else:
            icon = constants.ICON_BLANK

    return icon ,icon_value


def get_blender_icon_for_job_definition(job_definition: JobDefinition) -> str or int:
    icon_tuple = get_blender_icon_tuple_for_job_definition(job_definition)

    # if a custom icon has been returned use that
    if icon_tuple[1] > 0:
        return icon_tuple[1]

    # otherwise use the native blender icon
    return icon_tuple[0]
