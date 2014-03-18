"""JASMIN Cloud

Cloudhands ops functional tests vCloud 5.5 - test networking config - config
of Edge device
"""
__author__ = "P J Kershaw"
__date__ = "05/03/14"
__copyright__ = "(C) 2014 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__revision__ = "$Id$"
import sys
_py3 = sys.version_info >= (3, 0)

if _py3:
    from urllib.request import urlopen
    from urllib.request import Request
else:
    from urllib2 import urlopen, Request

from os import path, environ
import unittest
import re
import keyword
import logging
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

import xml.etree.ElementTree as ET

from libcloud import security
from libcloud.compute.types import Provider
import libcloud.compute.providers
from libcloud.compute.providers import get_driver
from libcloud.compute.drivers.vcloud import get_url_path, fixxpath

# Location of the directory containing *this* module
HERE_DIR = path.dirname(__file__)

# The configuration directory holds files for setting the vCD hostname and 
# user credentials, also, a CA directory for CA certificate bundle file
CONFIG_DIR = path.join(HERE_DIR, 'config')

# CA Certificates bundle for securing the connection to the server.  This is a
# concatenated set of PEM-format CA certificates.  Nb. server authentication is
# disabled in the test environment as the test server is using a selg-signed 
# certificate
CA_CERTS_PATH = path.join(CONFIG_DIR, 'ca', 'v55-ca-bundle.crt')

# File containing the authentication credentials.  It should be of the form
# <vCloud id>@<vCloud Org Name>:<password>
CREDS_FILEPATH = path.join(CONFIG_DIR, 'v55creds.txt')

# File containing the hostname for the vCloud Director API endpoint.  Simply
# place the FQDN on a single line and save the file.
CLOUD_HOSTNAME_FILEPATH = path.join(CONFIG_DIR, 'v55cloud-host.txt')

is_bool = lambda val: val.lower() in ('true', 'false')

def infer_type_from_str(val):
    if is_bool(val):
        return bool(val)
    
    # Try for an integer
    try:
        return long(val)
 
    except ValueError:
        # Check for floating point number
        try:
            return float(val)
        
        except ValueError:
            # Default to string
            return val

def mk_valid_varname(name):
    '''Make a valid Python variable name from XML element attributes'''
    if not isinstance(name, basestring):
        return None
    
    varname = camelcase2underscores(re.sub('[^0-9a-zA-Z_]', '_', name))

    # Avoid reserved names
    if keyword.iskeyword(varname):
        varname += '_'
        
    return varname

def camelcase2underscores(varname):
    to_underscores_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', varname)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', to_underscores_name).lower()
     
et_strip_ns_from_tag = lambda tagname: tagname.rsplit('}')[-1]
et_get_tagname = lambda elem: et_strip_ns_from_tag(elem.tag)

def _log_etree_elem(obj, level=logging.DEBUG):
    if log.getEffectiveLevel() <= level:
        log.debug(ET.tostring(obj))

    
class Vcd55TestCloudClient(unittest.TestCase):
    '''Test vCloud Director API v5.5 network configuration 
     
    '''
    USERNAME, PASSWORD = open(CREDS_FILEPATH).read().strip().split(':')
    CLOUD_HOSTNAME = open(CLOUD_HOSTNAME_FILEPATH).read().strip()
    
    # Disable SSL verification for testing ONLY
#    security.CA_CERTS_PATH = [CA_CERTS_PATH]
    security.VERIFY_SSL_CERT = False
    
    def setUp(self):
        '''Initialise vCD driver'''
        libcloud.compute.providers.DRIVERS[Provider.VCLOUD] = (
            "cloudhands.ops.test.functional.cloudclient.vcloud.patch.vcloud",
            "VCloud_5_5_NodeDriver"
        )

        driver = get_driver(Provider.VCLOUD)
        self.driver = driver(self.__class__.USERNAME,
                             self.__class__.PASSWORD, 
                             host=self.__class__.CLOUD_HOSTNAME,
                             api_version='5.5',
                             port=443)

    def test01(self):
        vdcs = self.driver.vdcs
        self.assert_(vdcs)
        
        for vdc in vdcs:
            log.info("vDC ID: %r", vdc.id)
            log.info("vDC Name: %r", vdc.name)
            log.info("vDC Driver: %r", vdc.driver)
            log.info("vDC Storage: %r", vdc.storage)
            log.info("vDC Memory: %r", vdc.memory)
            log.info("vDC CPU: %r", vdc.cpu)
            
        self._add_nat(vdc, '192.168.0.1', 'external ip')
        
    def _get_edgegateway(self, vdc):
        # Find out the Edge Gateway URIs for this VDC
        edgegateway_uris = self._get_vdc_edgegateway_uris(vdc.id)
        
        # Resolve the first to retrieve the Edge Gateway Record
        edgegateway_recs = self._get_edgegateway_rec(edgegateway_uris[0])
        
        # Resolve the Edge Gateway record link to get the Edge Gateway 
        # information
        return self._get_edgegateway_from_uri(edgegateway_recs[0].href)
      
    def _add_nat(self, vdc, org_ip, ext_ip):
        '''Add a new NAT to map from an internal organisation address to an
        external host
        '''
        gateway = self._get_edgegateway(vdc)
        
        # Alter the gateway settings adding a new NAT entry
        
        self._update_edgegateway(gateway)
        
    def _update_edgegateway(self, gateway):
        '''Update Edge Gateway with settings provided'''
        update_uri = None
        for link in gateway.link:
            if link.rel == 'edgeGateway:configureServices':
                update_uri = link.rel
                break
            
        if update_uri is None:
            self.fail('No Gateway update URI found in Gateway response')
            
        res = self.driver.connection.request(get_url_path(update_uri),
                                             method='POST',
                                             data=ET.tostring(gateway._elem))
              
    def _get_vdc_edgegateway_uris(self, vdc_uri):
        '''Get vDC Edge Gateway URIs'''
        edgegateway_uris = []
        for link in self._get_elems(vdc_uri, "Link"):
            if link.get('rel') == 'edgeGateways':
                edgegateway_uris.append(link.get('href'))
                
        return edgegateway_uris

    def _get_elems(self, uri, xpath):
        '''Get XML elements from a given URI and XPath search over returned XML 
        content
        '''
        res = self.driver.connection.request(get_url_path(uri))
        if xpath.startswith('{'):
            return res.object.findall(xpath)
        else:
            return res.object.findall(fixxpath(res.object, xpath))
           
    def _get_edgegateway_rec(self, edgegateway_uri):
        res = self.driver.connection.request(get_url_path(edgegateway_uri))
        _log_etree_elem(res.object)
#        
#        class EdgeGatewayRecord(object):
#            '''Edge gateway record'''
#
        edgegateway_rec_elems = res.object.findall(fixxpath(res.object, 
                                                   "EdgeGatewayRecord"))
        edgegateway_recs = []
        for edgegateway_rec_elem in edgegateway_rec_elems:
#            edgegateway_recs.append(EdgeGatewayRecord())
#            
#            for name, val in edgegateway_rec_elem.items():
#                
#                varname = mk_valid_varname(name)
#                if varname is not None:
#                    # Skips attributes which are namespace declarations
#                    setattr(edgegateway_recs[-1], 
#                            varname, 
#                            infer_type_from_str(val))
            edgegateway_recs.append(self._et_class_walker(edgegateway_rec_elem))
                   
        return edgegateway_recs
    
    def _get_edgegateway_from_uri(self, edgegateway_rec_uri):
        res = self.driver.connection.request(get_url_path(edgegateway_rec_uri))
        _log_etree_elem(res.object)
        
        gateway_iface_elems = res.object.findall(fixxpath(res.object, 
                                                          "GatewayInterface"))
        
        gateway = self._et_class_walker(res.object)
        
        # Augment gateway object with explicit reference to ElementTree elem
        gateway._elem = res.object
        
        return gateway
   
    def _et_class_walker(self, elem):
        '''Creates classes corresponding to elements and instantiates objects
        with attributes based on the element's attributes'''
        
        # Make a class with the same name as the XML element and instantiate
        _cls = type(et_get_tagname(elem), (object,), {})
        _obj = _cls()
        
        # Add the XML element's attributes as attributes of the new Python
        # object
        for attrname, attrval in elem.attrib.items():
            # Make a valid variable name from XML attribute name -
            # et_get_tagname() call strips out ElementTree namespace specifier
            # where needed
            varname = mk_valid_varname(et_strip_ns_from_tag(attrname))
            if varname is not None:
                setattr(_obj, varname, infer_type_from_str(attrval))
        
        # Check for a text setting for the XML element, if present add its
        # content as a new variable 'value_'
        if elem.text is not None:
            elem_text = elem.text.strip()
            if elem_text:
                setattr(_obj, 'value_', infer_type_from_str(elem_text))
            
        # Go to the next levels in XML hierarchy recursively adding further
        # child objects to _obj
        for child_elem in elem:
            
            # Check for duplicate element names - if so make an array of items
            if len(elem.findall(child_elem.tag)) > 1:
                # More than one XML child element of the same name is present
                
                # Create a Python variable name for it
                varname = camelcase2underscores(et_get_tagname(child_elem))
                
                # Check to see if the current object already has an attribute
                # with this name
                var = getattr(_obj, varname, None)
                if var is not None:
                    # List variable already exists - append to it
                    var.append(self._et_class_walker(child_elem))
                else:
                    # List variable doesn't exist - create it and populate with
                    # first element
                    setattr(_obj, 
                            varname, 
                            [self._et_class_walker(child_elem)])
            else:
                # Only one XML child element exists with this name
                setattr(_obj, 
                        camelcase2underscores(et_get_tagname(child_elem)), 
                        self._et_class_walker(child_elem))
            
        return _obj 
