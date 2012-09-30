from contextlib import contextmanager

from mock import MagicMock, patch, call
from nose.tools import istest

from provy.core.roles import DistroInfo
from provy.more.debian import ApacheRole, AptitudeRole
from tests.unit.tools.helpers import ProvyTestCase


class ApacheRoleTest(ProvyTestCase):
    def setUp(self):
        self.role = ApacheRole(prov=None, context={})

    @istest
    def installs_necessary_packages_to_provision(self):
        with self.using_stub(AptitudeRole) as aptitude:
            self.role.provision()

            aptitude.ensure_package_installed.assert_called_with('apache2')

    @istest
    def ensures_module_is_installed_and_enabled(self):
        with self.using_stub(AptitudeRole) as aptitude, self.execute_mock() as execute:
            self.role.ensure_mod('foo')

            aptitude.ensure_package_installed.assert_called_with('libapache2-mod-foo')
            execute.assert_called_with('a2enmod foo', sudo=True)

    @istest
    def ensures_site_is_available_and_enabled_from_template(self):
        with self.execute_mock() as execute, self.mock_role_method('update_file') as update_file, self.mock_role_method('remote_symlink') as remote_symlink:
            self.role.ensure_site('bar-website', file='/local/path/to/bar-website')

            update_file.assert_called_with('/local/path/to/bar-website', '/etc/apache2/sites-available/bar-website', options={}, sudo=True)
            remote_symlink.assert_called_with(from_file='/etc/apache2/sites-available/bar-website', to_file='/etc/apache2/sites-enabled/bar-website', sudo=True)
            execute.assert_called_with('service apache2 reload', sudo=True)

    @istest
    def ensures_site_is_available_and_enabled_from_template_and_options(self):
        with self.execute_mock() as execute, self.mock_role_method('update_file') as update_file, self.mock_role_method('remote_symlink') as remote_symlink:
            self.role.ensure_site('bar-website', file='/local/path/to/bar-website', options={'foo': 'Baz',})

            update_file.assert_called_with('/local/path/to/bar-website', '/etc/apache2/sites-available/bar-website', options={'foo': 'Baz',}, sudo=True)
            remote_symlink.assert_called_with(from_file='/etc/apache2/sites-available/bar-website', to_file='/etc/apache2/sites-enabled/bar-website', sudo=True)
            execute.assert_called_with('service apache2 reload', sudo=True)