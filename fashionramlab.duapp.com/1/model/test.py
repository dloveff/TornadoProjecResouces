#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from orm import Base
#from sqlalchemy import String, Integer, Column, ForeignKey
#from sqlalchemy.orm import relationship

#__author__ = 'chinfeng'

#class XUser(Base):
    #__tablename__='x_users'

    #id = Column(Integer,primary_key=True)
    #name = Column(String(255))
    #fullname = Column(String(255))
    #password = Column(String(255))
    #addresses = relationship("XAddress", order_by="XAddress.id", backref="user")

    #def __init__(self, name, fullname, password):
        #self.name = name
        #self.fullname = fullname
        #self.password = password


#class XAddress(Base):
    #__tablename__ = 'x_addresses'
    #id = Column(Integer, primary_key=True)
    #email_address = Column(String(255), nullable=False)
    #user_id = Column(Integer, ForeignKey('x_users.id'))
    ## 此关联跟上等价
    ## user = relationship("XUser", backref=backref('addresses', order_by=id))

    #def __init__(self, email):
        #self.email_address = email
