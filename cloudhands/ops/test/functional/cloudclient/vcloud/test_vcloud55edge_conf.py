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
    try:
        return long(val)
    
    except ValueError:
        if is_bool(val):
            return bool(val)
        else:
            return val

def mk_valid_varname(name):
    '''Make a valid Python variable name from XML element attributes'''
    if name.startswith('http'):
        # Ignore schema declarations
        return None
    
    varname = re.sub('[^0-9a-zA-Z_]', '_', name)

    # Avoid reserved names
    if keyword.iskeyword(varname):
        varname += '_'
        
    return varname

def camelcase2underscores(varname):
    to_underscores_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', varname)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', to_underscores_name).lower()
     
et_get_tagname = lambda elem: elem.tag.rsplit('}')[-1]
      
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
        
        edgegateway_uris = self._get_vdc_edgegateways(vdc.id)
        self.assert_(edgegateway_uris)
        
        edgegateway_recs = self._get_edgegateway_rec(edgegateway_uris[0])
        self.assert_(edgegateway_recs)
        
        edgegateway = self._resolve_edgegateway_rec_uri(
                                                    edgegateway_recs[0].href)
        self.assert_(edgegateway)
        
    def _get_vdc_network_with_urlopen(self, vdc_uri):
        '''Get vDC networks using urlopen'''
        try:
            headers = self.driver.connection.add_default_headers({})
            headers['User-Agent'] = self.driver.connection._user_agent()
            req = Request(vdc_uri, None, headers)
            vdc_fp = urlopen(req)
            log.info("Organisation info %s", vdc_fp.read())
            
        except Exception as e:
            self.fail(e)
            
    def _get_vdc_edgegateways(self, vdc_uri):
        '''Get vDC Edge Gateway URIs'''
        res = self.driver.connection.request(get_url_path(vdc_uri))
        self.assert_(res.object)
        _log_etree_elem(res.object)
        
        edgegateway_uris = []
        for link in res.object.findall(fixxpath(res.object, "Link")):
            if link.get('rel') == 'edgeGateways':
                edgegateway_uris.append(link.get('href'))
                
        return edgegateway_uris
    
    def _get_edgegateway_rec(self, edgegateway_uri):
        res = self.driver.connection.request(get_url_path(edgegateway_uri))
        _log_etree_elem(res.object)
        
        class EdgeGatewayRecord(object):
            '''Edge gateway record'''

        edgegateway_rec_elems = res.object.findall(fixxpath(res.object, 
                                                   "EdgeGatewayRecord"))
        edgegateway_recs = []
        for edgegateway_rec_elem in edgegateway_rec_elems:
            edgegateway_recs.append(EdgeGatewayRecord())
            
            for name, val in edgegateway_rec_elem.items():
                
                varname = mk_valid_varname(name)
                if varname is not None:
                    # Skips attributes which are namespace declarations
                    setattr(edgegateway_recs[-1], 
                            varname, 
                            infer_type_from_str(val))
                   
        return edgegateway_recs
    
    def _resolve_edgegateway_rec_uri(self, edgegateway_rec_uri):
        res = self.driver.connection.request(get_url_path(edgegateway_rec_uri))
        _log_etree_elem(res.object)
        
        gateway_iface_elems = res.object.findall(fixxpath(res.object, 
                                                          "GatewayInterface"))
        
        _obj = self._et_class_walker(res.object)
        return _obj
   
    def _et_class_walker(self, elem):
        '''Creates classes corresponding to elements and instantiates objects
        with attributes based on the element's attributes'''
        
        # Make a class with the same name as the XML element and instantiate
        _cls = type(et_get_tagname(elem), (object,), {})
        _obj = _cls()
        
        # Add the XML element's attributes as attributes of the new Python
        # object
        for attrname, attrval in elem.attrib.items():
            varname = mk_valid_varname(attrname)
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
