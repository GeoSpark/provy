#!/usr/bin/python
# -*- coding: utf-8 -*-

from getpass import getpass
import os


def provyfile_path_from(args):
    path = args[0]
    if not os.path.exists(path):
        raise IOError('provy file "%s" does not exist.' % path)
    if os.path.isabs(path):
        raise ValueError('provy file "%s" is absolute. Please provide a path that is relative to the current working directory.')
    return path


def import_module(module_name):
    module = __import__(module_name)
    if '.' in module_name:
        return reduce(getattr, module_name.split()[1:], module)
    return module


class AskFor(object):
    def __init__(self, key, question):
        self.key = key
        self.question = question

    def get_value(self, server):
        value = getpass("[Server at %s] - %s: " % (server['address'], self.question))
        return value
