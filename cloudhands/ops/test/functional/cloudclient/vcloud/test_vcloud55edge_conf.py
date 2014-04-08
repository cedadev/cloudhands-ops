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

from os import path
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

# Configuration for Edge Gateway NAT'ing - .cfg.dev file is used for testing
# .cfg checked into git
EDGE_GATEWAY_CONF_FILEPATH = path.join(CONFIG_DIR, 'edge_gateway.cfg.dev')


is_bool = lambda val: val.lower() in ('true', 'false')
bool2str = lambda val: str(val).lower()

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
et_get_namespace = lambda elem: elem.tag[1:].split("}", 1)[0]
et_mk_tag = lambda namespace, tagname: "{%s}%s" % (namespace, tagname)

def _log_etree_elem(obj, level=logging.DEBUG):
    if log.getEffectiveLevel() <= level:
        log.debug(ET.tostring(obj))


class GatewayNatRule(object):
    '''Gateway NAT rule'''
    IFACE_URI_TYPE = "application/vnd.vmware.admin.network+xml"
    DEFAULT_PORT = "any"
    DEFAULT_PROTOCOL = "any"
    
    def __init__(self,
                 iface_uri=None,
                 iface_name=None,
                 iface_uri_type=IFACE_URI_TYPE,
                 orig_ip=None,
                 orig_port=DEFAULT_PORT,
                 transl_ip=None,
                 transl_port=DEFAULT_PORT,
                 protocol=DEFAULT_PROTOCOL):
    
        self.iface_uri = iface_uri
        self.iface_name = iface_name
        self.iface_uri_type = iface_uri_type
        self.orig_ip = orig_ip
        self.orig_port = orig_port
        self.transl_ip = transl_ip
        self.transl_port = transl_port
        self.protocol = protocol
        
        
class NatRule(object):
    RULE_TYPES = ('DNAT', 'SNAT')
    
    def __init__(self, rule_type='DNAT', rule_id=None, rule_is_enabled=False,
                 **gateway_nat_rule_kw):
        self.rule_type = rule_type
        self.rule_id = rule_id
        self.rule_is_enabled = rule_is_enabled
        
        self.gateway_nat_rule = GatewayNatRule(**gateway_nat_rule_kw)
    
    @property
    def rule_type(self):
        return self._rule_type
    
    @rule_type.setter
    def rule_type(self, val):
        if val not in self.__class__.RULE_TYPES:
            raise ValueError('Accepted values for "rule_type" are: %r' %
                             self.__class__.RULE_TYPES) 

        self._rule_type = val
           
    
class Vcd55TestCloudClient(unittest.TestCase):
    '''Test vCloud Director API v5.5 network configuration 
     
    '''
    USERNAME, PASSWORD = open(CREDS_FILEPATH).read().strip().split(':')
    CLOUD_HOSTNAME = open(CLOUD_HOSTNAME_FILEPATH).read().strip()
    
    # Disable SSL verification for testing ONLY
#    security.CA_CERTS_PATH = [CA_CERTS_PATH]
    security.VERIFY_SSL_CERT = False
    
    CONFIG_EDGE_GATEWAY_URI = 'edgeGateway:configureServices'
    NAT_SERVICE_XPATH = ('Configuration/EdgeGatewayServiceConfiguration/'
                         'NatService')
    EDGE_GATEWAY_SERVICE_CONF_XPATH = \
                        'Configuration/EdgeGatewayServiceConfiguration'
             
    SRC_NAT_RULE_TYPE = 'SNAT'
    DEST_NAT_RULE_TYPE = 'DNAT'
    
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
        
        self._ns = None

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
      
    def _add_nat_rule(self, vdc, internal_ip, external_ip):
        '''Add a new NAT to map from an internal organisation address to an
        external host
        '''
        gateway = self._get_edgegateway(vdc)
        
        log.debug('Current EdgeGateway configuration . . . ')
        _log_etree_elem(gateway._elem)
        
        # Alter the gateway settings adding a new NAT entry
        
#        self._update_edgegateway(gateway)
        
    def _update_edgegateway(self, gateway, iface_name='EXT-INTERNET-TEST',
                            internal_ip='192.168.0.6',
                            external_ip='130.246.139.249'):
        '''Update Edge Gateway with settings provided'''
        
        # Find update endpoint
        update_uri = None
        for link in gateway.link:
            if link.rel == self.__class__.CONFIG_EDGE_GATEWAY_URI:
                update_uri = link.href
                break
            
        if update_uri is None:
            self.fail('No Gateway update URI found in Gateway response')
        
        self._ns = et_get_namespace(gateway._elem)
        
        # Get the update elements - the update interface expects a 
        # <EdgeGatewayServiceConfiguration/> top-level element
        gateway_service_conf_elem = gateway._elem.find(
                    fixxpath(gateway._elem,
                             self.__class__.EDGE_GATEWAY_SERVICE_CONF_XPATH))
        if gateway_service_conf_elem is None:
            self.fail('No <EdgeGatewayServiceConfiguration/> element found '
                      '<EdgeGateway/> settings returned from service')
            
        # Check allocation of external IPs
        
        # Get interface URI
        iface_uri = None
        for interface in \
                gateway.configuration.gateway_interfaces.gateway_interface:
            if interface.name.value_ == iface_name:
                iface_uri = interface.network.href
                break
            
        if iface_uri is None:
            self.msg('Interface found with name %r' % iface_name)

        # Check rule IDs already allocated
        highest_nat_rule_id = 0
        nat_service = \
            gateway.configuration.edge_gateway_service_configuration.nat_service
        for nat_rule in nat_service.nat_rule:
            if nat_rule.id.value_ > highest_nat_rule_id:
                highest_nat_rule_id = nat_rule.id.value_
                
        next_nat_rule_id = highest_nat_rule_id + 1

        # Check external IP is not already used in an existing rule
        # TODO: should this necessarily be a fatal error?
        for nat_rule in nat_service.nat_rule:
            gw_rule = nat_rule.gateway_nat_rule
            if (external_ip in (gw_rule.original_ip.value_, 
                                gw_rule.translated_ip.value_)):
                self.fail('Required external IP address %r has already been '
                          'used in an existing NAT rule (id %r)' %
                          (external_ip, nat_rule.id.value_))
        
        # Source NAT rule
        snat_rule = NatRule(rule_type=self.__class__.SRC_NAT_RULE_TYPE,
                            rule_id=str(next_nat_rule_id),
                            rule_is_enabled=True,
                            iface_uri=iface_uri,
                            iface_name=iface_name,
                            orig_ip=internal_ip,
                            transl_ip=external_ip)

       
        nat_service_elem = gateway._elem.find(
                    fixxpath(gateway._elem, self.__class__.NAT_SERVICE_XPATH))
        if nat_service_elem is None:
            self.fail('No <NatService/> element found in returned Edge Gateway '
                      'configuration')
            
        nat_service_elem.append(self._create_nat_rule(snat_rule))
        
        # Destination NAT rule
        next_nat_rule_id += 1
        dnat_rule = NatRule(rule_type=self.__class__.DEST_NAT_RULE_TYPE,
                            rule_id=str(next_nat_rule_id),
                            rule_is_enabled=True,
                            iface_uri=iface_uri,
                            iface_name=iface_name,
                            orig_ip=external_ip,
                            transl_ip=internal_ip)
                
        nat_service_elem.append(self._create_nat_rule(dnat_rule))
        
        _log_etree_elem(gateway._elem)
        
        # Despatch updated configuration
        gateway_service_conf_xml = ET.tostring(gateway_service_conf_elem)
        res = self.driver.connection.request(get_url_path(update_uri),
                                             method='POST',
                                             data=gateway_service_conf_xml)
        self.assert_(res)
        _log_etree_elem(res.object)

    def _create_nat_rule(self, nat_rule):   
        '''Create XML for a new NAT rule appending it to the NAT Service element
        '''                                                                       
        nat_rule_elem = ET.Element(et_mk_tag(self._ns, 'NatRule'))
        rule_type_elem = ET.SubElement(nat_rule_elem, et_mk_tag(self._ns, 
                                                                'RuleType'))
        rule_type_elem.text = nat_rule.rule_type
        
        is_enabled_elem = ET.SubElement(nat_rule_elem, 
                                        et_mk_tag(self._ns, 'IsEnabled'))
        is_enabled_elem.text = bool2str(nat_rule.rule_is_enabled)
        
        id_elem = ET.SubElement(nat_rule_elem, et_mk_tag(self._ns, 'Id'))
        id_elem.text = str(nat_rule.rule_id)
        
        gateway_nat_rule_elem = self._create_gateway_nat_rule_elem(
                                                    nat_rule.gateway_nat_rule)
        
        nat_rule_elem.append(gateway_nat_rule_elem)
        
        return nat_rule_elem
    
    def _create_gateway_nat_rule_elem(self, gateway_nat_rule):
        '''Make a NAT Rule gateway interface XML element
        '''
        gateway_nat_rule_elem = ET.Element(et_mk_tag(self._ns, 
                                                     'GatewayNatRule'))
        
        ET.SubElement(gateway_nat_rule_elem,
                      et_mk_tag(self._ns, 'Interface'),
                      attrib={
                         'href': gateway_nat_rule.iface_uri,
                         'name': gateway_nat_rule.iface_name,
                         'type': gateway_nat_rule.iface_uri_type
                      })
        
        orig_ip_elem = ET.SubElement(gateway_nat_rule_elem, 
                                     et_mk_tag(self._ns, 'OriginalIp'))
        orig_ip_elem.text = gateway_nat_rule.orig_ip
        
        orig_port_elem = ET.SubElement(gateway_nat_rule_elem, 
                                       et_mk_tag(self._ns, 'OriginalPort'))
        orig_port_elem.text = gateway_nat_rule.orig_port
        
        transl_ip_elem = ET.SubElement(gateway_nat_rule_elem, 
                                       et_mk_tag(self._ns, 'TranslatedIp'))
        transl_ip_elem.text = gateway_nat_rule.transl_ip
        
        transl_port_elem = ET.SubElement(gateway_nat_rule_elem, 
                                         et_mk_tag(self._ns, 'TranslatedPort'))
        transl_port_elem.text = gateway_nat_rule.transl_port
        
        protocol_elem = ET.SubElement(gateway_nat_rule_elem, 
                                      et_mk_tag(self._ns, 'Protocol'))
        protocol_elem.text = gateway_nat_rule.protocol
        
        return gateway_nat_rule_elem
                   
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

        edgegateway_rec_elems = res.object.findall(fixxpath(res.object, 
                                                   "EdgeGatewayRecord"))
        edgegateway_recs = []
        for edgegateway_rec_elem in edgegateway_rec_elems:
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
        
        # Make a class with the same name as the XML element and instantiate.
        # Trailing underscore flags that this class was created dynamically
        _cls = type(et_get_tagname(elem) + '_', (object,), {})
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
