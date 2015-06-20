#! /usr/bin/env python
# -*- coding: utf-8 -*-

from meta import ModuleMetaClass

class ModuleBase(object):
    __metaclass__ = ModuleMetaClass
    
    __module_name__ = 'undefined'
    __module_version__ = '0.0.0'
    
    __module_template__ = 'nomodule.html'
        
    #def __init__(self, name, serial=None):
        #session = getSession()
        #self.module_model = session.query(Module).filter(Module.serial == serial).first()
        #if not self.module_model:
            #cls = '%s.%s' % (self.__module__, self.__name__)
            #self.module_model = Module(cls, name, uuid4().hex)
            #session.add(self.module_model)
            #session.commit()
            
        #self.__module_name__ = name
        #self.__module_serial__ = serial
        #self.__module_id__ = self.module_model.id
        