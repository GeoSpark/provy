from contextlib import contextmanager
from unittest import TestCase

from mock import MagicMock, patch, call
from nose.tools import istest

from provy.more.debian import MySQLRole


FOO_DB_WITH_JOHN_GRANTS = """
*************************** 1. row ***************************
Grants for john@%: GRANT USAGE ON *.* TO 'john'@'%' IDENTIFIED BY PASSWORD '*B9EE00DF55E7C816911C6DA56F1E3A37BDB31093'
*************************** 2. row ***************************
Grants for john@%: GRANT ALL PRIVILEGES ON `foo`.* TO 'john'@'%'
"""
FOO_DB_WITHOUT_JOHN_GRANTS = """
*************************** 1. row ***************************
Grants for john@%: GRANT USAGE ON *.* TO 'john'@'%' IDENTIFIED BY PASSWORD '*B9EE00DF55E7C816911C6DA56F1E3A37BDB31093'
"""


class MySQLRoleTest(TestCase):
    def setUp(self):
        self.role = MySQLRole(prov=None, context={})

    @istest
    def has_no_grant_if_not_granted(self):
        with patch('provy.core.roles.Role.execute') as execute:
            execute.return_value = FOO_DB_WITHOUT_JOHN_GRANTS
            self.assertFalse(self.role.has_grant('ALL', 'foo', 'john', '%', False))

    @istest
    def has_grant_if_granted(self):
        with patch('provy.core.roles.Role.execute') as execute:
            execute.return_value = FOO_DB_WITH_JOHN_GRANTS
            self.assertTrue(self.role.has_grant('ALL', 'foo', 'john', '%', False))
