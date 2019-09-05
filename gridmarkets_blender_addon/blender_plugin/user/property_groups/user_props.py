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
from gridmarkets_blender_addon import constants


class UserProps(bpy.types.PropertyGroup):

    AUTH_EMAIL_DESCRIPTION = "Your " + constants.COMPANY_NAME + " account email"
    AUTH_KEY_DESCRIPTION = "Your " + constants.COMPANY_NAME + " access key. This is different from your " \
                           "password and can be found by opening the " + constants.COMPANY_NAME + " manager " \
                           "portal and viewing your profile details"

    # user's email
    auth_email = bpy.props.StringProperty(
        name="Email",
        description=AUTH_EMAIL_DESCRIPTION,
        default="",
        maxlen=1024,
    )

    # user's access key
    auth_accessKey = bpy.props.StringProperty(
        name="Access Key",
        description=AUTH_KEY_DESCRIPTION,
        default="",
        maxlen=1024,
        subtype='PASSWORD'
    )
