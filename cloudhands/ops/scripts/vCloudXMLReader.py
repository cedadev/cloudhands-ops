__author__ = 'cl'

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring

class vCloudXMLReader:

    def __init__(self):
        #Allowing the caller to set the namespace would give better abstraction.
        #self.namespaces = {'vm':'http://www.vmware.com/vcloud/v1.5',
        #'ovf':'http://schemas.dmtf.org/ovf/envelope/1'}
        self.namespaces = {'vcloud':'http://www.vmware.com/vcloud/v1.5', 'ovf':'http://schemas.dmtf.org/ovf/envelope/1'}

    def parseFile(self, xmlFile):
        self.dom = ET.parse(xmlFile)
    def parseString(self, xmlStr):
        self.dom = ET.fromstring(xmlStr)

    def getElements(self, elem):
        return self.dom.findall(elem,self.namespaces)

    def getAttrValue(self, elem, attr):
        for e in self.getElements(elem):
            return e.get(attr)

    def getElementsList(self, elem):
        arr = self.dom.iterfind(elem,self.namespaces)
        return arr

    def getAttrValueList(self, elem, attr):
        vcd_item_list = list()
        for e in self.getElementsList(elem):
            vcd_item_list.append(e.get(attr))
        return vcd_item_list

#    def getAttrRefList(self, elem):
#        vcd_item_list = list()
#        for e in self.getElementsList(elem):
#            vcd_item = vcdRef(e.get('name'), e.get('href'))
#            vcd_item_list.append(vcd_item)
#        return vcd_item_list

    def getElementContent(self, elem):
        #Guessing you want to return a list of these bad boys.
        for e in self.getElements(elem):
            #This gives the text content of the Element.
            return e.text

    def dump(self):
        print(self.dom)