#!/usr/bin/env python

class ParserPattern:



    def __init__(self):
        self.__transalteTypePlantUmlTojson = {
            "String":{'basicType':'string','format':'','pattern':''},
            "Number":{'basicType':'number','format':'','pattern':''},
            "Int":{'basicType':'integer','format':'','pattern':''},
            "Boolean":{'basicType':'boolean','format':'','pattern':''},
            "Timestamp":{'basicType':'string','format':'utc-millisec','pattern':''},
            "Date":{'basicType':'string','format':'date','pattern':''},
            "Datetime":{'basicType':'string','format':'date-time','pattern':''},
            "GUID":{'basicType':'string','format':'','pattern':'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'}
        }
        self._patternsCollection=['Collection']
        self._patternsDocument=['Document']
        self._patternsEntity=['Entity']
        self._patternsEmbeddedEntity=['EmbeddedEntity']
        self._patternsRelatedEntitity=['RelatedEntitity']
        self._patternsRelatedField=['RelatedList','RelatedId','RelatedListRq']
        self._patternsIsRequired=['embeddedListRq','embeddedListRqIdx', 'embeddedRq', 'idxRequired', 'AzureSearchRq', 'required','fieldListRq','fieldListRqIdx','RelatedListRq']
        self._patternsIsIndex=['idxRequired', 'indexed', 'AzureSearchRq', 'AzureSearch','fieldListRqIdx','fieldListIdx','embeddedListRqIdx','embeddedListIdx']
        self._patternsIsKey= ['idKey']
        self._patternsRegularField=['field','fieldList','fieldListRq','fieldListRqIdx','fieldListIdx']
        self._patternsIsEmbedded=['embeddedListRq','embeddedListIdx','embeddedListRqIdx','embeddedList', 'embeddedRq', 'embedded']
        self._patternsIsEnumerationBlock=['EnumDefBlock']
        self._patternsEnum=['Enum']
        self._patternNote= 'note as N'
        self._patternTipology='Typology'
        self._patternReferencing='referencing'
        self._patternEtag='_etag'
        self._patternSelf='_self'
        self._patternTTL='ttl'
        self._patternContentTypeValue= 'application/json;com.wba.inventory.{}.{}.{}'
        self._patternContentType= 'contentType'



    def get_typeJson(self,pltumltype):
        properties = self.__transalteTypePlantUmlTojson[pltumltype]
        return properties['basicType']

    def get_formatJson(self,pltumltype):
        properties = self.__transalteTypePlantUmlTojson[pltumltype]
        return properties['format']

    def get_patternJson(self,pltumltype):
        properties = self.__transalteTypePlantUmlTojson[pltumltype]
        return properties['pattern']

    def capitalize(self,strConv):
        rework=''
        if strConv is not None:
            firstChar=strConv[:1]
            rework=firstChar.upper() + strConv[1:]
        return  rework
