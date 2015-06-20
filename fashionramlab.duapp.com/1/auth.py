#! /usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from tornado.web import HTTPError

def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.get_current_user():
            raise HTTPError(401)
        return method(self, *args, **kwargs)
    return wrapper