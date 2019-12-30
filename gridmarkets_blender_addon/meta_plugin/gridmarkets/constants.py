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

COMPANY_NAME = "GridMarkets"
ROOT_ATTRIBUTE_ID = "GM_PROJECT_NAME"

ENUM_SUBTYPE_PRODUCT_VERSIONS = "PRODUCT_VERSIONS"
BLENDER_VERSIONS_ENUM_ID = "BLENDER_VERSION"


class PRODUCTS:
    BLENDER = "blender"
    VRAY = "vray"


class BLENDER_VERSIONS:
    V_2_81A = "2.81a"
    V_2_80 = "2.80"
    V_2_79B = "2.79b"


class BLENDER_ENGINES:
    CYCLES = "CYCLES"
    EEVEE = "EEVEE"
    INTERNAL = "INTERNAL"


class VRAY_VERSIONS:
    V_3_60_03 = "3.60.03"
    V_3_60_04 = "3.60.04"
    V_3_60_05 = "3.60.05"
    V_4_02_05 = "4.02.05"
    V_4_10_01 = "4.10.01"
    V_4_10_02 = "4.10.02"


class ATTRIBUTE_NAMES:
    PRODUCT = "app"