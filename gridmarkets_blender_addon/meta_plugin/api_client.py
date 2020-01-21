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

from abc import ABC, abstractmethod
import typing

from gridmarkets_blender_addon.meta_plugin.user import User
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject
from gridmarkets_blender_addon.meta_plugin.plugin_accessor import PluginAccessor
from gridmarkets_blender_addon.meta_plugin.job_preset import JobPreset
from gridmarkets_blender_addon.meta_plugin.api_schema import APISchema

from gridmarkets_blender_addon.meta_plugin.errors.invalid_email_error import InvalidEmailError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_access_key_error import InvalidAccessKeyError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_user_error import InvalidUserError

if typing.TYPE_CHECKING:
    from .product import Product
    from .factory_collection import FactoryCollection
    from .user_info import UserInfo
    from .machine_option import MachineOption


class APIClient(ABC, PluginAccessor):

    def __init__(self):
        self._signed_in_user = None

    def sign_in(self, user: User, skip_validation: bool = False) -> None:

        if not skip_validation:
            try:
                self.validate_credentials(user.get_auth_email(), user.get_auth_key())
            except InvalidEmailError as e:
                raise e
            except InvalidAccessKeyError as e:
                raise e
            except InvalidUserError as e:
                raise e

        self._signed_in_user = user

        # add the user to the saved profiles list if not already added
        user_container = self.get_plugin().get_preferences_container().get_user_container()
        profiles = user_container.get_all()

        for profile in profiles:
            if profile.get_auth_email() == user.get_auth_email() and profile.get_auth_key() == user.get_auth_key():
                return None

        user_container.append(user)

    def sign_out(self) -> None:
        self._signed_in_user = None

    def is_user_signed_in(self) -> bool:
        return self._signed_in_user is not None

    @abstractmethod
    def connected(self) -> bool:
        raise NotImplementedError

    def get_signed_in_user(self) -> typing.Optional[User]:
        if self.is_user_signed_in():
            return self._signed_in_user
        return None

    @abstractmethod
    def get_api_schema(self, factory_collection: 'FactoryCollection') -> APISchema:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def validate_credentials(auth_email: str, auth_access_key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def upload_project(self,
                       packed_project: PackedProject,
                       upload_root_dir: bool,
                       delete_local_files_after_upload: bool = False) -> RemoteProject:
        raise NotImplementedError

    @abstractmethod
    def submit_new_project(self,
                           packed_project: PackedProject,
                           job_preset: JobPreset,
                           delete_local_files_after_upload: bool = False) -> RemoteProject:
        raise NotImplemented

    @abstractmethod
    def submit_to_remote_project(self,
                                 remote_project: RemoteProject,
                                 job_preset: JobPreset) -> None:
        raise NotImplemented

    @abstractmethod
    def update_remote_project_status(self, remote_project: RemoteProject) -> None:
        raise NotImplemented

    @abstractmethod
    def get_products(self, ignore_cache=False) -> typing.List['Product']:
        raise NotImplementedError

    @abstractmethod
    def get_products_with_app_type(self, app_type: str) -> typing.List['Product']:
        raise NotImplementedError

    @abstractmethod
    def get_product_app_types(self, ignore_cache=False) -> typing.List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_user_info(self, ignore_cache=False) -> 'UserInfo':
        raise NotImplementedError

    @abstractmethod
    def get_machines(self,
                     app: str,
                     operation: str,
                     ignore_cache: bool = False) -> typing.List['MachineOption']:
        raise NotImplementedError

