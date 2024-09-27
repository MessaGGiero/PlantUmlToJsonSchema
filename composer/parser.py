#!/usr/bin/env python
from customexception.contractexception import *
from composer.documentPlantUml import *
from composer.parserPattern import ParserPattern

import  re

__author__ = "Massimo Iannuzzi"
__copyright__ = "free use"
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Massimo Iannuzzi"
__email__ = ""
__status__ = "Develop"


class Parser(ParserPattern):

    def __init__(self):
        super(Parser,self).__init__()

    def __findTag(self,tagSearch,statment):
        """
        :param tagSearch: Tag to search
        :param lines: list file lines where the searchn is applied
        :return:
        """
        searchString='^{}\b*\(.*'.format(tagSearch)

        retTag=re.search(searchString, statment.strip())
        return retTag

    #deprecated
    def __searchPattern(self,statment,targetList):

        if (statment is None):
            raise ErrorTypeArgument('Param statment is nullable')

        if (type(statment) is not str):
            raise ErrorTypeArgument('Param statment is not string: {}'.format(type(statment)))

        retPattern=None
        for pattern in targetList:
            if (self.__findTag(str(pattern),statment) !=None):
                retPattern=True
                break

        return retPattern



    def __searchAndReturnPattern(self,statment,targetList):

        if (statment is None):
            raise ErrorTypeArgument('Param statment is nullable')

        if (type(statment) is not str):
            raise ErrorTypeArgument('Param statment is not string: {}'.format(type(statment)))

        retPattern=None
        for pattern in targetList:
            if (self.__findTag(pattern,statment) !=None):
                retPattern=pattern
                break

        return retPattern


    def __findTagPosition(self,patternSearch,documentLines):
        """
        :param tagSearch: Tag to search
        :param documentLines: list file lines where the searchn is applied
        :return:
        """
        return [idx for idx, s in enumerate(documentLines) if  self.__findTag(patternSearch,s.strip())]


    def __extractBlock(self,tag,startPosition,lines):
        blockTag=[]
        balance=0

        if tag not in str(lines[startPosition:]):
            raise ErrorTypeParser('The block to parse is not a {} )'.format(tag))

        if '{' not in str(lines[startPosition:]):
            raise ErrorTypeParser('The block package is not correct')

        if '}' not in str(lines[startPosition:]):
            raise ErrorTypeParser('The block package is not correct')

        for line in lines[startPosition:]:
            if '{' in line:
                balance=balance+1

            if '}' in line:
                balance=balance-1

            blockTag.append(line)
            if balance == 0:
                break
        return blockTag

    def __testParamDocumentLines(self,plantFileLines):

        if plantFileLines is None:
            raise ErrorTypeArgument('Param plantFileLines is None')

        if type(plantFileLines) is not list:
            raise ErrorTypeArgument('Param documentLines is invalide  type: {}'.format(type(plantFileLines)))

    def __extractNote(self,tag,startPosition,lines):

        if tag not in str(lines[startPosition:]):
            raise ErrorTypeParser('The block to parse is not a {} )'.format(tag))

        pkFLag=False
        ukFlag=False
        compIFlag=False
        thrgFlag=False
        uniquekeys=''
        partiyionKey=''
        composeIndex=None
        for line in lines[startPosition:]:

            if 'end note'.lower() in line.lower():
                break

            if 'Partition Key'.lower() in line.lower():
                pkFLag=True
                continue

            if 'Unique Key'.lower() in line.lower():
                ukFlag=True
                continue

            if 'Throughput'.lower() in line.lower():
                thrgFlag=True
                continue

            if 'Composite Indexes'.lower() in line.lower():
                compIFlag=True
                continue

            if pkFLag:
                partiyionKey=line
                pkFLag=False

            if ukFlag:
                uniquekeys=line
                ukFlag=False

            if thrgFlag:
                #Nothing
                thrgFlag=False

            if compIFlag:
                composeIndex=line
                compIFlag=False

        #masian
        tmpSplit=partiyionKey.split()
        if tmpSplit is None or len(tmpSplit) <2:
            raise ErrorTypeArgument('Invalid Notes : invalid  Partition Key')

        partitionKeyName=tmpSplit[0].strip()
        partitionKeyType=tmpSplit[1].strip().replace('"','')
        if self._patternTipology in partitionKeyType:
            regx='.*' + self._patternTipology + '\b*\((.*)\).*'
            match=re.search(regx, partitionKeyType)
            partitionKeyType=match.group(1) if match else None
            if partitionKeyType is None:
                raise ErrorTypeParser('Invalid Notes: invalid ')

        noteInfo=NoteInfo(partitionKeyName,partitionKeyType,uniquekeys,composeIndex)
        return noteInfo

    def isIdKey(self,statment):
        return self.__searchPattern(statment, self._patternsIsKey)

    def isRequired(self,statment):
        return self.__searchPattern(statment,self._patternsIsRequired)

    def isRequiredRetPattern(self,statment):
        return self.__searchAndReturnPattern(statment,self._patternsIsRequired)


    def isIndex(self, statment):
        return self.__searchPattern(statment,self._patternsIsIndex)


    def isIndexdRetPattern(self,statment):
        return self.__searchAndReturnPattern(statment,self._patternsIsIndex)


    def isRegularField(self, statment):
        return self.__searchPattern(statment,self._patternsRegularField)


    def isRegularFieldRetPattern(self,statment):
        return self.__searchAndReturnPattern(statment,self._patternsRegularField)


    def isEmbedded(self,statment):
            return self.__searchPattern(statment, self._patternsIsEmbedded)

    def isEmbeddedRetPattern(self,statment):
        return self.__searchAndReturnPattern(statment, self._patternsIsEmbedded)


    def isEnumerationBlock(self,statment):
        return self.__searchPattern(statment, self._patternsIsEnumerationBlock)


    def isEnumerationBlockRetPattern(self,statment):
        return self.__searchAndReturnPattern(statment, self._patternsIsEnumerationBlock)

    def isRelated(self,statment):
        return self.__searchPattern(statment,self._patternsRelatedField)

    def isRelatedRetPattern(self,statment):
        return self.__searchAndReturnPattern(statment,self._patternsRelatedField)

    def extractCollectionInfo(self,documentLines):
        '''

        :param documentLines:
        :return: dict collectionInfo
        '''

        self.__testParamDocumentLines(documentLines)
        tagSearch=str(self._patternsCollection[0])
        collectionBlockStart=self.__findTagPosition(tagSearch,documentLines)

        if (collectionBlockStart is None) or (len(collectionBlockStart)==0) or (len(collectionBlockStart)>1):
            raise ErrorTypeArgument('Invalid Document file: invalid  {}'.format(self._patternsCollection))

        startPos=collectionBlockStart[0]

        collectionBlockDefinition=self.__extractBlock(tagSearch,startPos,documentLines)

        if collectionBlockDefinition is None:
            raise ErrorTypeArgument('Invalid Document file: invalid  bad Collection Definition')

        header=collectionBlockDefinition[0]
        count_comma = header.count(',')
        if count_comma == 3:
            regx = tagSearch + '.*\(\b*(.*)\b*\,\b*(.*)\b*\,\b*(.*)\b*\,\b*(.*)\).*{'
        elif count_comma == 4:
            regx = tagSearch + '.*\(\b*(.*)\b*\,\b*(.*)\b*\,\b*(.*)\b*\,\b*(.*)\b*\,\b*(.*)\).*{'
        else:
            raise ErrorTypeArgument('Invalid Document file: invalid  bad Collection Definition')

        match = re.search(regx, header)

        if match is None:
            raise ErrorTypeArgument('Invalid Document file: invalid  bad Collection Definition')

        collName=match.group(1)
        collConsistency=match.group(2)

        collPartitionKey=match.group(3)
        if collPartitionKey is not None:
            collPartitionKey = collPartitionKey.strip()

        collOptimistic=match.group(4)
        if collOptimistic is not None:
            collOptimistic = collOptimistic.strip()

        ttl = None
        if count_comma == 4:
            ttl=match.group(5)

        if ttl is not None:
            ttl = ttl.strip()

        collectionInfo = CollectionInfo(collName,collConsistency,collPartitionKey,collOptimistic,ttl)

        return collectionInfo

    def extractEnumDefBlock(self,documentLines):

        '''
        :param documentLines:
        :return: list of dict
        '''

        self.__testParamDocumentLines(documentLines)


        tagSearch=str(self._patternsIsEnumerationBlock[0])
        enumBlockStart=self.__findTagPosition(tagSearch,documentLines)

        if ((enumBlockStart is None) or (len(enumBlockStart)==0) or (len(enumBlockStart)>1)):
            raise ErrorTypeArgument('Invalid Document file: invalid  {}'.format(tagSearch))

        startPos=enumBlockStart[0]
        enumBlockDefinition=self.__extractBlock(tagSearch,startPos,documentLines)
        tagSearch=str(self._patternsEnum[0])
        listIdxEnum=self.__findTagPosition(tagSearch,enumBlockDefinition)
        listEnumerations=[]

        for startPos in listIdxEnum:
            enumDefinition=self.__extractBlock(tagSearch,startPos,enumBlockDefinition)
            tmpEnum=''.join(enumDefinition)
            enumName=''
            enumDescription=''
            enumList=''
            #regx=tagSearch+'.*\((.*)\,(.*){(.*)}'
            regx=tagSearch+'.*\((.*)\).*{(.*)}'
            match=re.search(regx, tmpEnum)
            tmpContent = match.group(1) if match else None
            if (tmpContent is not None):
                tmpSplit=tmpContent.split(',')
                if tmpSplit is None or len(tmpSplit) == 0:
                    raise ErrorTypeArgument('Invalid Document file: invalid  {}'.format(tagSearch))
                enumName=tmpSplit[0].strip()
                enumDescription=tmpSplit[1].strip().replace('"','')
            else:
                raise ErrorTypeArgument('Invalid Document file: invalid  {}'.format(tagSearch))
            #enumName=match.group(1) if match else None
            #enumDescription=match.group(2) if match else None
            enumList=match.group(2) if match else None
            enumDescription= enumDescription.replace('"','') if enumDescription is not None else ''
            enumDef = EnumDefBlock(enumName,enumDescription,enumList)
            listEnumerations.append(enumDef)

        return listEnumerations



    def extractNoteInfo(self,documentLines):

        self.__testParamDocumentLines(documentLines)

        tagSearch=self._patternNote

        noteBlockStart=[idx for idx, s in enumerate(documentLines) if  re.search('^{}'.format(tagSearch),s.strip())]

        if (noteBlockStart is None) or (len(noteBlockStart)==0) or (len(noteBlockStart)>1):
            raise ErrorTypeArgument('Invalid Document file: invalid  {}'.format(tagSearch))

        startPos=noteBlockStart[0]

        noteDefinition=self.__extractNote(tagSearch,startPos,documentLines)

        if noteDefinition is None:
            raise ErrorTypeArgument('Invalid Document file: invalid  bad note Definition')

        return noteDefinition

    def extractGenericBlock(self,documentLines,typeTag):


        if documentLines is None or len(documentLines) == 0:
            raise ErrorTypeParser('Empty block to parser')
        header=documentLines[0]
        #print ('Header: ',header)
        #regx=typeTag+'.*\((.*)\,.*(.*)\)'

        name=None
        name2=None
        regx=typeTag+'.*\((.*)\,.*'
        match=re.search(regx, header)
        name=match.group(1) if match else None
        regx=typeTag+'.*\(.*,(.*)\){'
        match=re.search(regx, header)
        name2=match.group(1) if match else None
        if name==None:
            regx=typeTag+'.*\((.*)\).*'
            match=re.search(regx, header)
            name=match.group(1) if match else None


        if name is None:
            raise ErrorTypeParser('Parsing error on block {}'.format(typeTag))

        blck=Block(name,typeTag)

        for row in documentLines[1:]:
            isReq=False  # required
            isEmb=False  # embedded
            isIdx=False  # index
            isFld=False  # field
            isArr=False  # array
            isTpl=False  # tipology
            isKey=False  # key
            isRlt=False  # related

            if len(row.strip()) == 0 or  re.match("^==.*",row) or re.match("^/.*",row) or re.match("^--.*",row) or re.match("\b*}\b*",row) or re.match("\b*{\b*",row):
                continue

            if self.isIdKey(row):
                isKey=True

            if self.isRequired(row):
                isReq=True

            if self.isIndex(row):
                isIdx=True

            if self.isEmbedded(row):
                isEmb=True

            if self.isRegularField(row):
                isFld=True

            if self.isRelated(row):
                isRlt=True

            #Extract
            nameField=None
            typeName=None
            embeddedType=None
            if isEmb :
                regx='.*\((.*)\,(.*)\)'
                match=re.search(regx, row)
                nameField=match.group(1) if match else None
                typeName=match.group(2) if match else None
                embeddedType = self.isEmbeddedRetPattern(row)
                if nameField is None or typeName is None or len(typeName) == 0 or len(nameField)==0:
                    raise ErrorTypeParser('Parser bad block {}'.format(row))
                if 'List' in embeddedType:
                    isArr=True
            elif isRlt:
                regx='.*\((.*)\,(.*)\)'
                match=re.search(regx, row)
                nameField=match.group(1) if match else None
                typeName=match.group(2) if match else None
                relatedType = self.isRelatedRetPattern(row)
                if nameField is None or typeName is None or len(typeName) == 0 or len(nameField)==0:
                    raise ErrorTypeParser('Parser bad block {}'.format(row))
                if 'List' in relatedType:
                    isArr=True
            else:
                #particular case regular filed in (fieldList,fieldListRq,fieldListRqIdx,fieldListIdx)
                relatedType = self.isRegularFieldRetPattern(row)
                if isFld and ('List' in relatedType):
                    regx='.*\((.*)\,(.*)\)'
                    match=re.search(regx, row)
                    nameField=match.group(1) if match else None
                    typeName=match.group(2) if match else None
                    isArr=True
                else:
                    #othes case: field/required/idxRequired(xx) primitive or field/required/idxRequired(xx) tipology
                    tmpParts=row.split()
                    if tmpParts is None or len(tmpParts)<2:
                        raise ErrorTypeParser('Parser bad block {}'.format(row))

                    regx='.*\((.*)\)\b*(.*)'
                    match=re.search(regx, tmpParts[0])
                    nameField=match.group(1) if match else None
                    typeName=tmpParts[1]

                    if nameField is None or typeName is None or len(typeName) == 0 or len(nameField)==0:
                        raise ErrorTypeParser('Parser bad block {}'.format(row))
                    #Particular case for Typology type
                    if self._patternTipology in typeName:
                        regx='.*' + self._patternTipology + '\b*\((.*)\).*'
                        match=re.search(regx, typeName)
                        typeName=match.group(1) if match else None
                        if typeName is None:
                            raise ErrorTypeParser('Parser bad block {}'.format(row))
                        isTpl=True

                    #Particular case for referencing type
                    if self._patternReferencing in typeName:
                        typeName="String"

            blck.addField(nameField,typeName,isIdx,isReq,isTpl,isEmb,isArr,isKey,isRlt,isFld)
        return blck;

    def extractDocumentDefBlock(self,documentLines):
        '''
        :param documentLines:
        :return: list
        '''

        documentList=[]
        self.__testParamDocumentLines(documentLines)
        tagSearchDocument=str(self._patternsDocument[0])
        DocumentStarts=self.__findTagPosition(tagSearchDocument,documentLines)

        if (DocumentStarts is None) or (len(DocumentStarts)==0):
            raise ErrorTypeArgument('Invalid Document file: invalid  {}'.format(tagSearchDocument))

        for startPos in DocumentStarts:

            #get Documenti info header example name
            documentBlockDefinition=self.__extractBlock(tagSearchDocument,startPos,documentLines)

            nameDocument=None
            contentType=None
            # Check for old plant-uml whithout version on contract
            regx=self._patternsDocument[0]+'\b*\((.*)\)\b*{'
            match=re.search(regx, documentBlockDefinition[0])
            if match is not None and match.group(1).find(',')==-1:
                #Old contract
                nameDocument=match.group(1)
            else:
                #New contract
                regx=self._patternsDocument[0]+'\b*\(\b*(.*),\b*(.*),\b*(.*)\b*\)\b*{'
                match=re.search(regx, documentBlockDefinition[0])
                if match is None:
                    raise ErrorTypeArgument('Invalid Document file: invalid  {}'.format(tagSearchDocument))
                nameDocument=match.group(1)
                domain=match.group(2)
                version_contract=match.group(3)
                contentType = self._patternContentTypeValue.format(domain, nameDocument, version_contract)


            if (nameDocument is None):
                raise ErrorTypeParser('Invalid document Block: {}'.format(documentBlockDefinition[0]))

            document=Document(nameDocument,contentType)
            blck=None
            #Blocco Lavorazione delle Entity
            tagSearch=str(self._patternsEntity[0])
            documentPosEntity=self.__findTagPosition(tagSearch,documentBlockDefinition)
            if (documentPosEntity is None) or (len(documentPosEntity)==0):
                raise ErrorTypeParser('Invalid Entity Block')
            for startEntity in documentPosEntity:
                blckEntity=self.__extractBlock(tagSearch,startEntity,documentBlockDefinition)
                blck=self.extractGenericBlock(blckEntity,tagSearch)

            if blck is not None:
                document.addBlock(blck)

            #Blocco Lavorazione delle EmbeddedEntity
            blck=None
            tagSearch=str(self._patternsEmbeddedEntity[0])
            documenEmbeddedtEntity=self.__findTagPosition(tagSearch,documentBlockDefinition)
            if (documenEmbeddedtEntity is not None) or (len(documenEmbeddedtEntity)!=0):
                for startEmbedded in documenEmbeddedtEntity:
                    blckEntity=self.__extractBlock(tagSearch,startEmbedded,documentBlockDefinition)
                    blck=self.extractGenericBlock(blckEntity,tagSearch)
                    if blck is not None:
                        document.addBlock(blck)

            #Blocco Lavorazione delle RelatedEntity
            blck=None
            #Blocco lavorazione related entity (documenRelatedtEntity)
            tagSearch=str(self._patternsRelatedEntitity[0])
            documenRelatedEntitity=self.__findTagPosition(tagSearch,documentBlockDefinition)
            if (documenRelatedEntitity is not None) or (len(documenRelatedEntitity)!=0):
                for startEmbedded in documenRelatedEntitity:
                    blckRelatedEntity=self.__extractBlock(tagSearch,startEmbedded,documentBlockDefinition)
                    blck=self.extractGenericBlock(blckRelatedEntity,tagSearch)
                    if blck is not None:
                        document.addBlock(blck)
            documentList.append(document)


        return documentList