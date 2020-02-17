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

import typing

from gridmarkets_blender_addon import utils_blender
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.meta_plugin.gridmarkets.remote_project import RemoteProject


# todo create remote project subclass
def get_blender_icon_tuple_for_remote_project(remote_project: RemoteProject) -> typing.Tuple[str, int]:
    product = remote_project.get_attribute(api_constants.API_KEYS.APP)
    return utils_blender.get_product_logo(product)


def get_blender_icon_for_remote_project(remote_project: RemoteProject) -> str or int:
    icon_tuple = get_blender_icon_tuple_for_remote_project(remote_project)

    # if a custom icon has been returned use that
    if icon_tuple[1] > 0:
        return icon_tuple[1]

    # otherwise use the native blender icon
    return icon_tuple[0]
