#!/usr/bin/env python

from customexception.contractexception import *
import json
import os
import string

__author__ = "Massimo Iannuzzi"
__copyright__ = "free use"
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Massimo Iannuzzi"
__email__ = ""
__status__ = "Develop"


class CollectionInfo:
    def __init__(self,name,consistency,partitionkey,optimistic,ttl):
        if consistency is None or partitionkey is None or optimistic is None :
            raise ErrorTypeParser('CollectionInfo mandatory attributes')
        self.__consistency = consistency
        self.__partitionkey = partitionkey
        self.__optimistic = optimistic
        self.__name = name
        self.__ttl = ttl

    def get_name(self):
        return self.__name

    def get_consistency(self):
        return self.__consistency

    def get_partitionkey(self):
        return self.__partitionkey

    def get_optimistic(self):
            return self.__optimistic

    def set_name(self,name):
        self.__name = name

    def set_partiyionKey(self,partiyionKey):
        self.__partiyionKey=partiyionKey

    def set_consistency(self,consistency):
        self.__consistency=consistency

    def set_partiyionKey(self,optimistic):
        self.__optimistic=optimistic

    def get_ttl(self):
        return self.__ttl

class NoteInfo:

    def __init__(self,partiyionKey,partiyionKeyType,uniquekeys='',composeIndex=None):
        if partiyionKey is None or partiyionKeyType is None:
            raise ErrorTypeParser('NoteInfo mandatory attributes')
        self.__partiyionKey = partiyionKey
        self.__uniquekeys = uniquekeys
        self.__partiyionKeyType=partiyionKeyType
        self.__composeIndex=composeIndex

    def get_partiyionKey(self):
        return self.__partiyionKey

    def get_partiyionKeyType(self):
            return self.__partiyionKeyType

    def get_uniquekeys(self):
        return self.__uniquekeys

    def get_composeIndex(self):
        return  self.__composeIndex

    def set_partiyionKey(self,partiyionKey):
        self.__partiyionKey=partiyionKey

    def set_uniquekeys(self,uniquekeys):
        self.__uniquekeys=uniquekeys

    def set_composeIndex(self,composeIndex):
        self.__composeIndex=composeIndex

class EnumDefBlock:

    def __init__(self,name,description,constants):

        if name is None or constants is None:
            raise ErrorTypeParser('EnumDefBlock mandatory attributes')
        self.__name = name;
        self.__constants=constants
        self.__description=description

    def get_name(self):
        return self.__name

    def get_description(self):
            return self.__description

    def get_constants(self):
            return self.__constants

    def set_name(self,name):
        self.__name=name

    def set_description(self,description):
        self.__description=description

    def set_constants(self,constants):
        self.__constants=constants

class Block():

    keyName='name'
    keyType='typefield'
    keyIsIndex='isindexed'
    keyIsTypology='istypology'
    keyIsRequired='isrequired'
    keyIsArray='isarray'
    KeyIsEmbedded='isembedded'
    KeyIsKey='iskey'
    KeyIsRelated='isrelated'
    KeyIsRegular='isregular'

    def __init__(self,name,blocktype):

        if name is not None or blocktype is not None:
            self.__name=name
            self.__blocktype=blocktype
        else:
            raise ErrorTypeArgument("Mandatory parm for Block costructr class")
        self.__fields=[]

    def addField(self,name,typeField,isindexed,isrequired,istypology,isembedded,isarray,iskey,isrelated,isregular):

        if name is None or typeField is None:
            raise ErrorTypeArgument("entity param null")

        self.__fields.append({'name':name,'typefield':typeField,'isindexed':isindexed,'isrequired':isrequired,'istypology':istypology,'isembedded':isembedded,'isarray':isarray,'iskey':iskey,'isrelated':isrelated,'isregular':isregular})

    def getName(self):
        return self.__name

    def getFields(self):
        return self.__fields

    def getblocktype(self):
        return self.__blocktype

class Document:

    def __init__(self,name,content_type=None):
        if name is not None:
            self.__name=name
        else:
            raise ErrorTypeArgument("Mandatory parm for Domcumet costructr class")
        self.__listBlock=[]
        self.__content_type=content_type


    def addBlock(self,block):

        if type(block) is not Block:
            raise ErrorTypeArgument("embeddedEntitity param null")
        self.__listBlock.append(block)

    def getListBlock(self):
        return self.__listBlock

    def getName(self):
        return self.__name

    def getContentType(self):
        return self.__content_type