#!/usr/bin/env python

from composer.parser import Parser
from customexception.contractexception import *
from composer.contract import *
from composer.parserPattern import ParserPattern
from composer.policyindex import PolicyIndex
from datetime import datetime
import plantumltojschemagui
import shutil


__author__ = "Massimo Iannuzzi"
__copyright__ = "free use"
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Massimo Iannuzzi"
__email__ = ""
__status__ = "Develop"

class Composer(ParserPattern):

    #General declaration
    __plantUmlDocument=[]
    __enumDirectory='enums'
    __embeddedDirectory='embedded'

    def __init__(self,plantUmlDoc,objGui=None):

        super(Composer,self).__init__()

        if type(plantUmlDoc) is not list:
            raise  ErrorTypeParser('Parser Erorre: Not valid plantUml document')

        if ((plantUmlDoc is None) or (len(plantUmlDoc)== 0)):
            raise  ErrorTypeParser('Parser Erorre: Not valid plantUml document')

        self.__plantUmlDocument=[s.strip() for s in plantUmlDoc]
        self.__objGui=objGui

    @property
    def get__plantUmlDocument(self):
        return self.__plantUmlDocument


    def __writeOnGui(self,strPrint):
        if self.__objGui is not None:
            self.__objGui.writeLog(strPrint)
        else:
            print(strPrint)

    def __isPolicyIndex(self):
        if self.__objGui is not None:
            return self.__objGui.isPolicyIndex()
        else:
            return True

    def __isPolicyIndexInternal(self):
        if self.__objGui is not None:
            return self.__objGui.isPolicyIndexInternal()
        else:
            return False

    def __createDir(self,rootDir,subDir):

        objpath = os.path.join(rootDir, subDir)
        if os.path.exists(objpath) and os.path.isdir(objpath):
            shutil.rmtree(objpath)
            os.mkdir(objpath)
        else:
            os.mkdir(objpath)
        return objpath

    def __updateMainContractFiles(self,listMainContracts,outputdir,policyIndex):

        if listMainContracts is None or len(listMainContracts) == 0:
            raise ErrorTypeParser('Parser Error list Main contract undefined')

        if policyIndex is None:
            raise ErrorTypeParser('Parser Error policy index undefined')

        #Update the contract file
        for mainContract in listMainContracts:
            contractName=mainContract.getContractName()
            contractPathName=os.path.join(outputdir, contractName)
            with open(contractPathName) as json_file:
                dataContract = json.load(json_file)

            if dataContract is None:
                raise ErrorTypeParser('Parser Error read main Contract for update index')

            if self.__isPolicyIndexInternal():
                dataContract['cosmos.policy'] = policyIndex.getPolicyJson()
            else:
                del dataContract['cosmos.policy']

            with open(os.path.join(outputdir,contractPathName), 'w') as outfile:
                json.dump(dataContract,outfile,indent=4)

        if self.__isPolicyIndex():
            policyIndex.dumpfile()



    def composerGenerator(self,outputdir):

        #Declariont block

        #Instance class for parsing plant-uml model
        parser=Parser()

        #Store only main contracts file for policy index generation
        listMainContracts=[]

        #define enumPath for typology
        enumPath=''
        #define embedded path for object
        embeddedPath=''

        #print("Start parser ...")
        self.__writeOnGui('Start parser {} ...'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        #Parsing Steps


        #
        # Step 1 Manage collection info
        #
        self.__writeOnGui('Start Collection info parsing...')

        collectionInfo=parser.extractCollectionInfo(self.__plantUmlDocument)
        collectionName=collectionInfo.get_name()
        collectionConsistency=collectionInfo.get_consistency()
        collectionOptimistic=collectionInfo.get_optimistic()
        collection_ttl = collectionInfo.get_ttl()

        #proposal add prefixto dir name for enums and embedded
        indexPos=collectionName.find('_')
        if indexPos == -1:
            raise ErrorTypeParser('Parser Error invalid collection name {}'.format(collectionName))
        indexPos=indexPos + 1
        prefixName=collectionName[indexPos:]
        self.__enumDirectory='enums' + prefixName.lower()
        self.__embeddedDirectory='embedded' + prefixName.lower()
        #End proposal

        #Mandatory create the output directory:
        #Check if enum directory exist and delete it and recreate
        embeddedPath=self.__createDir(outputdir, self.__embeddedDirectory)
        #Check if enum directory exist and delete it and recreate
        enumPath=self.__createDir(outputdir, self.__enumDirectory)


        #
        # Step 2 Manage Enumerations
        #

        #Store all enumeration in dictionary for consultation
        self.__writeOnGui('Start Enumeration processing ...')

        blockEnumDefs=parser.extractEnumDefBlock(self.__plantUmlDocument)
        for enum in blockEnumDefs:
            nameTypology=enum.get_name()
            nameTypology=self.capitalize(nameTypology)
            constants=[const.strip() for const in enum.get_constants().split(',')]
            typology=TipologyContract(nameTypology)
            typology.add_enum(constants)
            typology.add_description(enum.get_description())
            #Store tipology in subfolder enum
            typology.dumpfile(enumPath)

        #
        # Step 3 Manage notes
        #
        self.__writeOnGui('Start notes parsing ...')

        notes=parser.extractNoteInfo(self.get__plantUmlDocument)
        partitionKey=notes.get_partiyionKey()
        partitionkeyType=notes.get_partiyionKeyType().strip()
        composeIndex=notes.get_composeIndex()
        uniquekey=notes.get_uniquekeys()

        #Show message if in model are present th compose index declared
        #This index must be inserted manually in policy index file.
        if composeIndex is not  None:
            self.__writeOnGui('Warning: Composed indexes are present in the plantUml model. Manage these manually.')

        if uniquekey is not  None and len(uniquekey) > 0:
            self.__writeOnGui(f'Warning: Attention, there is a uniquekey: {uniquekey}. Manage these manually.')


        #
        # Step 4 Manage Document entity/embedded/related
        #
        listDocuments=parser.extractDocumentDefBlock(self.__plantUmlDocument)
        contract=None
        fileExt=''
        for document in listDocuments:
            #Estract general info from document
            documentName=document.getName()
            content_type = document.getContentType()
            #Estract list generic block
            blockList=document.getListBlock()

            prefPathTypology=''
            prefPathEmbedded=None
            #A generic block : Entity - EmbeddedEntity - RelatedEntitity
            for block in blockList:

                self.__writeOnGui('Parser Block Name: {}'.format(block.getName()))

                #If block is a Entity
                if block.getblocktype() in str(self._patternsEntity[0]):

                    documentName=self.capitalize(documentName)
                    contract = DocumentContract(documentName,collectionConsistency,'1.0')
                    contract.setCosmosCollection(collectionName)
                    if content_type is not None:
                        jsonField={}
                        jsonField["type"]="string"
                        jsonField["default"]=content_type
                        contract.addProperties(self._patternContentType,jsonField)

                    jsonField={}
                    jsonField['cosmos.id'] = True
                    jsonField['type'] = 'string'
                    contract.addProperties('id',jsonField)
                    jsonField={}
                    jsonField['type']=self.get_typeJson(partitionkeyType)
                    jsonField['cosmos.partitionKey']=True
                    jsonField['cosmos.index'] = True
                    if len(self.get_patternJson(partitionkeyType))>0:
                        jsonField['pattern']=self.get_patternJson(partitionkeyType)
                    contract.addProperties(partitionKey,jsonField)
                    contract.addRequiredField(partitionKey)
                    # Manage _etag for optmistic lock enable
                    if (collectionOptimistic.lower() == 'yes'):
                        jsonField={}
                        jsonField['type'] = 'string'
                        contract.addProperties(self._patternEtag,jsonField)

                    # Manage ttl for ttl on document
                    if (collection_ttl is not None) and (collection_ttl.lower() == 'yes'):
                        jsonField={}
                        jsonField['type'] = 'integer'
                        contract.addProperties(self._patternTTL,jsonField)

                    #Patch for adding _self techincal field
                    #01-07-2020
                    jsonField={}
                    jsonField['type'] = 'string'
                    contract.addProperties(self._patternSelf,jsonField)
                    #01-07-2020
                    #Store the contract for policy index file generation
                    listMainContracts.append(contract)
                    fileExt='Contract.json'

                elif (block.getblocktype() in str(self._patternsEmbeddedEntity[0])) or (block.getblocktype() in str(self._patternsRelatedEntitity[0])):
                    prefPathTypology='../'
                    prefPathEmbedded='./'
                    contract = EmbeddedContract(self.capitalize(block.getName()))
                    fileExt='.json'
                else:
                    raise ErrorTypeParser('Parser Error invalid block {}'.format(block.getblocktype()))

                for field in block.getFields():
                    jsonField={}

                    linkType=field[block.keyType]
                    linkType=self.capitalize(linkType.strip())

                    #Typology type
                    if field[block.keyIsTypology]:
                        jsonField['type']='object'
                        if linkType.endswith('Typology'):
                            jsonField['$ref'] = prefPathTypology + self.__enumDirectory + '/' + linkType + '.json'
                        else:
                            jsonField['$ref'] = prefPathTypology + self.__enumDirectory + '/' + linkType + 'Typology.json'
                    #Embedded Block
                    elif field[block.KeyIsEmbedded]:
                        if field[block.keyIsArray]:
                            jsonField['type'] = 'array'
                            items={}
                            #link=field[block.keyType]
                            #Case that the block is embedded ma the link is Typology. This particular case
                            if linkType.endswith('Typology'):
                                jsonField['items']={'$ref': prefPathTypology + self.__enumDirectory + '/' + linkType + '.json'}
                            else:
                                #In this case not is typology but is embedded with ref to other embedded
                                if prefPathEmbedded is  None:
                                    jsonField['items']={'$ref': self.__embeddedDirectory + '/' + linkType + '.json'}
                                else:
                                    #This is case that link must be stay in some thirectory
                                    jsonField['items']={'$ref': prefPathEmbedded + linkType + '.json'}
                        else:
                            jsonField['type'] = 'object'
                            #Case that the block is embedded ma the link is Typology. This particular case
                            if linkType.endswith('Typology'):
                                jsonField['$ref']= prefPathTypology + self.__enumDirectory + '/' + linkType + '.json'
                            else:
                                #In this case not is typology but is embedded with ref to other embedded
                                if prefPathEmbedded is None:
                                    jsonField['$ref']= self.__embeddedDirectory + '/' + linkType + '.json'
                                else:
                                    #This is case that link must be stay in some thirectory
                                    jsonField['$ref']= prefPathEmbedded + linkType + '.json'

                    #Related Block
                    elif field[block.KeyIsRelated]:
                        if field[block.keyIsArray]:
                            jsonField['type'] = 'array'
                            jsonField['items']={'type':'string'}
                        else:
                            jsonField['type'] = 'string'
                    #Regular field and of array type
                    elif field[block.KeyIsRegular] and field[block.keyIsArray]:
                        jsonField['type'] = 'array'
                        jsonField['items']={'type':self.get_typeJson(linkType)}
                    else:
                        jsonField['type'] = self.get_typeJson(linkType)
                        if len(self.get_formatJson(linkType))>0:
                            jsonField['format']=self.get_formatJson(linkType)
                        if len(self.get_patternJson(linkType))>0:
                            jsonField['pattern']=self.get_patternJson(linkType)

                    if field[block.keyIsIndex]:
                            jsonField['cosmos.index'] = True

                    #patch for old plant
                    if field[block.KeyIsKey]:
                        jsonField['cosmos.id'] = True

                    contract.addProperties(field[block.keyName],jsonField)

                    #Check if field is required
                    if field[block.keyIsRequired]:
                       contract.addRequiredField(field[block.keyName])


                if len(contract.getRequiredField()) == 0:
                    contract.removeRequired()

                rawJon=contract.getContractObj()
                if 'cosmos.collection' in rawJon:
                    contract.dumpfile(outputdir)
                else:
                    contract.dumpfile(os.path.join(outputdir,self.__embeddedDirectory))


        #if self.__isPolicyIndex() or self.__isPolicyIndexInternal():

        self.__writeOnGui('Generation Policy index file starting ...')
        #Parsing block looking for cosmox index in tree
        policy=PolicyIndex(outputdir,collectionName,self.__objGui)
        for mainContract in listMainContracts:
            contractName=mainContract.getContractName()
            policy.createPolicyindex(contractName)

        #Update the contract file
        self.__updateMainContractFiles(listMainContracts,outputdir,policy)



        self.__writeOnGui('Parsing completed {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))