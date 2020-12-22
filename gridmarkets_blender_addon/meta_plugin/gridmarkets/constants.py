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

"""
BLENDER_2_80_MAIN_PROJECT_FILE = "BLENDER_2_80_MAIN_PROJECT_FILE"
BLENDER_2_80_RENDER_ENGINE = "BLENDER_2_80_RENDER_ENGINE"
BLENDER_2_79_MAIN_PROJECT_FILE = "BLENDER_2_79_MAIN_PROJECT_FILE"
BLENDER_2_79_RENDER_ENGINE = "BLENDER_2_79_RENDER_ENGINE"
"""


class PROJECT_ATTRIBUTE_IDS:
    PROJECT_NAME = ROOT_ATTRIBUTE_ID
    PRODUCT = "PRODUCT"
    BLENDER_VERSION = "BLENDER_VERSION"
    VRAY_VERSION = "VRAY_VERSION"
    MAYA_VERSION = "MAYA_VERSION"


class JOB_DEFINITION_IDS:
    BLENDER_2_8X_CYCLES = 'BLENDER_2_8X_CYCLES'


class API_KEYS:
    PROJECT_NAME = "project_name"
    APP = "app"
    APP_VERSION = "app_version"
    PATH = "path"
    FRAMES = "frames"
    OUTPUT_PREFIX = "output_prefix"
    OUTPUT_FORMAT = "output_format"
    REMOTE_OUTPUT_FOLDER_NAME = "remote_output_folder_name"
    LOCAL_DOWNLOAD_PATH = "local_download_path"
    AUTO_DOWNLOAD = "auto_download"
    RENDER_ENGINE = "engine"
    GPU = "gpu"
    MACHINE_TYPE = "machine_type"
    INSTANCES = "instances"
    PROJECT_TYPE_ID = "project_type_id"


class SUBTYPE_KEYS:
    class STRING:
        class PATH:
            FILE_MODE = "FILE_MODE"
            FILE_PATH = "FILE_PATH"
            DIR_PATH = "DIR_PATH"

    class ENUM:
        class PRODUCT_VERSIONS:
            PRODUCT = "PRODUCT"
            MATCH = "MATCH"

        class MACHINE_TYPE:
            PRODUCT = "PRODUCT"
            OPERATION = "OPERATION"
            USE_GPU_DEFAULT = "USE_GPU_DEFAULT"


class PRODUCTS:
    BLENDER = "blender"
    VRAY = "vray"
    MOE = "moe"
    MAYA = "maya"


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
