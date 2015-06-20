#! /usr/bin/env python
# -*- coding: utf-8 -*-

from meta import PluginMetaClass


class PluginBase(object):
    __metaclass__ = PluginMetaClass
    name = 'undefined'

    def response_message(self, request=None):
        raise NotImplementedError('Abstract method not implemented.')