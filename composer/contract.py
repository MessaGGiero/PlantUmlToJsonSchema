#!/usr/bin/env python

from customexception.contractexception import *
import json
import os
import string

__author__ = "Massimo Iannuzzi"
__copyright__ = "free use"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Massimo Iannuzzi"
__email__ = ""
__status__ = "Develop"

class TipologyContract:

    def __init__(self,contractName):
        if contractName is None:
            raise ErrorTypeArgument('Typology contract: name reguired')
        self.__contractName=contractName
        self.__jsonContract={
            "$schema": "http://json-schema.org/draft-07/schema",
            "description": "Generic Type",
            "type": "string",
            "enum": []
        }

    def add_enum(self,constants):
        if type(constants) is not list:
            raise ErrorTypeArgument('Typology contract: wrong list constants')
        self.__jsonContract["enum"]=constants

    def add_description(self,description):
        if description is None:
            raise ErrorTypeArgument('Typology contract: wrong list constants')
        self.__jsonContract["description"]=description

    def getContract(self):
        return self.__jsonContract


    def dumpfile(self,outputDir):
        if outputDir is None or outputDir=='':
            raise ErrorTypeArgument('Output dir directory is not present in TypologyContract')
        outfileName=''
        if self.__contractName.endswith('Typology'):
            outfileName=self.__contractName
        else:
            outfileName=self.__contractName+'Typology'
        with open(os.path.join(outputDir,outfileName+'.json'), 'w') as outfile:
            json.dump(self.__jsonContract, outfile,indent=4)


class EmbeddedContract:
    def __init__(self,contractName):
        if contractName is None:
            raise ErrorTypeArgument('Typology contract: name reguired')
        self.__contractName = contractName
        self.__jsonContract={
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": self.__contractName,
            "description": "Schema json for "+self.__contractName,
            "type": "object",
            "properties": {},
            "required": []
            }

    def getContractName(self):
        return self.__contractName

    def getContractObj(self):
        return self.__jsonContract

    def dumpfile(self,outputDir):
        if outputDir is None or outputDir=='':
            raise ErrorTypeArgument('Output dir directory is not present in TypologyContract')
        with open(os.path.join(outputDir,self.__contractName+'.json'), 'w') as outfile:
            json.dump(self.__jsonContract, outfile,indent=4)

    def __isExist(self,nameProperty):
        if nameProperty in  self.__jsonContract['properties']:
            return True
        else:
            return False
            str = self.__jsonContract['properties']

    def addRequiredList(self,requiredList):
        """
        :param requiredList: list of string
        :return:
        """
        if type(requiredList) is not list:
            raise ErrorTypeArgument('Param requiredList is not corret: {}'.format(type(requiredList)))
        requireds = self.__jsonContract['required']
        for item in requiredList:
            requireds.append(item)

    def addRequiredField(self,field):
        '''
        :param field:
        :return:
        '''
        requireds = self.__jsonContract['required']
        requireds.append(field)

    def getRequiredField(self):
        return self.__jsonContract['required'];

    def removeRequired(self):
        del self.__jsonContract['required'];

    def addProperties(self,name,block):

        properties = self.__jsonContract['properties']
        if name not in properties:
            properties[name]=block
        else:
            raise ErrorTypeArgument('Parser Error duplicate property "{}" in model'.format(name))

    def updateTitle(self,title):
        self.__jsonContract['title'] = title

    def updateDescription(self,description):
        self.__jsonContract['description'] = description



class DocumentContract:

    def __init__(self,contractName,consistency,version='1.0'):
        self.__contractName = contractName
        self.__jsonContract = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": self.__contractName,
            "description": "Schema json for " + self.__contractName,
            "type": "object",
            "version": version,
            "cosmos.collection": "MSABBRE_serviceName",
            "cosmos.policy": {
            },
            'properties':{},
            "required":[]
        }
        self.__contractName = contractName

    def getContractName(self):
        return self.__contractName + 'Contract.json'

    def getContractObj(self):
        return self.__jsonContract

    def dumpfile(self,outputDir=''):
        if outputDir is None or outputDir=='':
            raise ErrorTypeArgument('Output dir directory is not present in argument')
        with open(os.path.join(outputDir,self.__contractName + 'Contract.json'), 'w') as outfile:
            json.dump(self.__jsonContract, outfile,indent=4)

    def __isExist(self,nameProperty):
        if nameProperty in  self.__jsonContract['properties']:
            return True
        else:
            return False
            str = self.__jsonContract['properties']

    def addRequiredList(self,requiredList):
        """
        :param requiredList: list of string
        :return:
        """
        if type(requiredList) is not list:
            raise ErrorTypeArgument('Param requiredList is not corret: {}'.format(type(requiredList)))
        requireds = self.__jsonContract['required']
        for item in requiredList:
            requireds.append(item)

    def addRequiredField(self,field):
        '''
        :param field:
        :return:
        '''
        requireds = self.__jsonContract['required']
        try:
            requireds.index(field)
        except:
            requireds.append(field)

    def getRequiredField(self):
        return self.__jsonContract['required'];

    def removeRequired(self):
        del self.__jsonContract['required'];

    def addProperties(self,name,block):

        properties = self.__jsonContract['properties']
        if name not in properties:
            properties[name]=block
        else:
            raise ErrorTypeArgument('Parser Error duplicate property "{}" in model'.format(name))


    def updateTitle(self,title):
        self.__jsonContract['title'] = title

    def updateDescription(self,description):
        self.__jsonContract['description'] = description

    def updateVersion(self,version):
        self.__jsonContract['version'] = version

    def setCosmosCollection(self,collecionName):
        self.__jsonContract['cosmos.collection'] = collecionName

    def getCosmosCollection(self):
        return self.__jsonContract['cosmos.collection']