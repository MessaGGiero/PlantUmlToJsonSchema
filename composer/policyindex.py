#!/usr/bin/env python

import json
import os

__author__ = "Massimo Iannuzzi"
__copyright__ = "free use"
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Massimo Iannuzzi"
__email__ = ""
__status__ = "Develop"

class PolicyIndex:

    def __init__(self,filesContractPath,collectionName,objGui=None):
        self.__objGui=objGui
        self.__defpolicy={
            "indexingMode": "consistent",
            "automatic": True,
            "includedPaths": [],
            "excludedPaths": [
                {
                    "path": "/*"
                },
                {
                    "path": "/\"_etag\"/?"
                }
            ]
        }

        self.__filesContractPath=filesContractPath
        self.__collectionName=collectionName

    def getPolicyJson(self):
        return self.__defpolicy

    def __getPolicyTemplate(self):

        return self.__defpolicy

    def __writeOnGui(self,strPrint):
        if self.__objGui is not None:
            self.__objGui.writeLog(strPrint)
        else:
            print(strPrint)

    def __existPath(self,includedPaths,path):
        ret=False
        for elem in includedPaths:
            for key in elem.keys():
                if key == 'path':
                    strCmp=elem[key]
                    if ( strCmp == path):
                        ret=True
        return  ret

    def __policyIndex(self,tracepath,pathFile,policy):
        basedir=os.path.dirname(pathFile)

        with open(pathFile) as json_file:
            data = json.load(json_file)

            for p in data['properties']:
                map=data['properties'][p]

                if 'cosmos.index' in map.keys():

                    polMap={"path": "/?", "indexes": []}
                    path=tracepath+p+'/?'
                    if not self.__existPath(policy['includedPaths'],path):
                        polMap['path'] = path
                        policy['includedPaths'].append(polMap)

                elif '$ref' in map.keys() and ('Typology' not in map['$ref']):

                    tmpPath=tracepath+p+'/'
                    #11-10-2019 commented
                    #tmpFileRef=map['$ref'].replace('.','',1).replace('/','')
                    tmpFileRef=map['$ref']
                    tmpFileName=os.path.join(basedir, tmpFileRef)
                    self.__policyIndex(tmpPath,tmpFileName,policy)

                elif 'items' in map.keys() and ('$ref' in map['items'].keys()) and ('Typology' not in map['items']['$ref']):

                    tmpPath=tracepath+p+'/'
                    if (map['type']=='array'):
                        tmpPath=tmpPath+'[]/'
                    #11-10-2019 commented
                    #tmpFileRef=map['items']['$ref'].replace('.','',1).replace('/','')
                    tmpFileRef=map['items']['$ref']
                    tmpFileName=os.path.join(basedir, tmpFileRef)
                    self.__policyIndex(tmpPath,tmpFileName,policy)


    def createPolicyindex(self,contractName):
        policyTemplate=self.__getPolicyTemplate()
        contractPathName=os.path.join(self.__filesContractPath, contractName)
        self.__writeOnGui('Policy index parsing for contract file {} '.format(contractName))
        self.__policyIndex('/',contractPathName,policyTemplate)


    def dumpfile(self):
        outputDir=self.__filesContractPath
        policyIndexFileDump='policy_{}.json'.format(self.__collectionName)
        with open(os.path.join(outputDir,policyIndexFileDump), 'w') as outfile:
            json.dump(self.__defpolicy,outfile,indent=4)
        self.__writeOnGui('Created file Policy index :  {} '.format(policyIndexFileDump))
