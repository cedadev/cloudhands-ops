"""JASMIN Cloud

Cloudhands ops functional tests vCloud 5.5 Apache libcloud tests
"""
__author__ = "P J Kershaw"
__date__ = "05/03/14"
__copyright__ = "(C) 2014 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__revision__ = "$Id$"
try:
    from urllib.request import urlopen
    from urllib.request import Request
    
except ImportError:
    from urllib2 import urlopen, Request

from os import path, environ
import unittest

import logging
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

from libcloud import security
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


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

@unittest.skip("Site-specific code. To go into cloudhands-jasmin.")
class Vcd55TestCloudClient(unittest.TestCase):
    '''Test vCloud Director API v5.5 against Apache Libcloud - requires
    patched version of the latter: 
    
     * copy the vcloud module from the patch sub-directory into the equivalent
     location for your libcloud installation i.e. replace 
     
    `libcloud.compute.drivers.vcloud`
    '''
    USERNAME, PASSWORD = open(CREDS_FILEPATH).read().strip().split(':')
    CLOUD_HOSTNAME = open(CLOUD_HOSTNAME_FILEPATH).read().strip()
    
    # Pick image name from environment variable or accept default
    IMAGE_NAME = environ.get(
                        'TEST_CLOUD_CLIENT_IMAGE_NAME') or 'stemcell-test' #'centos6-stemcell'
    
    NETWORK_NAME = environ.get('TEST_CLOUD_CLIENT_NETWORK_NAME') or \
                                                'proxied-external-network'
    
    EX_SCRIPT_FILEPATH = path.join(CONFIG_DIR, 'ex_script.sh')
    
    # Disable SSL verification for testing ONLY
#    security.CA_CERTS_PATH = [CA_CERTS_PATH]
    security.VERIFY_SSL_CERT = False
    
    def setUp(self):
        
#        libcloud.compute.providers.DRIVERS[Provider.VCLOUD] = (
#        "cloudhands.ops.test.functional.cloudclient.vcloud.patch.vcloud",
#        "VCloud_5_5_NodeDriver")

        driver = get_driver(Provider.VCLOUD)
        self.driver = driver(self.__class__.USERNAME,
                             self.__class__.PASSWORD, 
                             host=self.__class__.CLOUD_HOSTNAME,
                             api_version='5.5',
                             port=443)

    def _get_image(self):
        '''Query for images and return set by class var'''
        images = self.driver.list_images()

        for image in images:
            if image.name == self.__class__.IMAGE_NAME:
                return image   
                     
        self.fail('No %r image found in list of images available: %r' % 
                  (self.__class__.IMAGE_NAME, images))

    def _check_node(self, node):
        nodes = self.driver.list_nodes()
        
        for i in nodes:
            if i.name == node.name:
                return
            
        self.fail('No new node %r found in listing' % node.name)
               
    def test01_check_ca_bundle(self):
        self.assert_(security.CA_CERTS_PATH, 'No CA bundle set')
        log.info(security.CA_CERTS_PATH)
                
    def test02_list_vdcs(self):
        vdcs = self.driver.vdcs
        self.assert_(vdcs)
        
        for i in vdcs:
            log.info("vDC ID: %r", i.id)
            log.info("vDC Name: %r", i.name)
            log.info("vDC Driver: %r", i.driver)
            log.info("vDC Storage: %r", i.storage)
            log.info("vDC Memory: %r", i.memory)
            log.info("vDC CPU: %r", i.cpu)
        
    def test03_list_nodes(self):
        nodes = self.driver.list_nodes()
        self.assert_(nodes)
        for node in nodes:
            self.assert_(node)
            log.info(node)
            log.info(node.extra['vdc'])
            for vm in node.extra['vms']:
                log.info("VM name: %r", vm['name'])
                log.info("VM Operating system: %r", vm['os_type'])
                log.info("VM state: %r", vm['state'])
                log.info("VM private IPs: %r", vm['private_ips'])
                log.info("VM public IPs: %r", vm['public_ips'])
        
    def test04_list_images(self):
        # List all available vApp Templates
        images = self.driver.list_images()
        log.info('Images ...')
        for image in images:
            self.assert_(image)
            log.info(image)

    def test05_list_locations(self):
        locations = self.driver.list_locations()
        self.assert_(locations, 'No locations returned')
        
    def test05a_get_networks(self):
        networks = self.driver.networks
        for network in networks:
            log.info('network: %r, %r' % (network.attrib['name'], 
                                          network.attrib['href']))
            
            # Check network status
            try:
                headers = self.driver.connection.add_default_headers({})
                headers['User-Agent'] = self.driver.connection._user_agent()
                req = Request(network.attrib['href'], None, headers)
                network_fp = urlopen(req)
                log.info("network content %r", network_fp.read())
            except Exception as e:
                self.fail(e)
                    
    def test06_create_and_destroy_node(self):
        # Query images
        image = self._get_image()

        vapp_name = 'phil-test06_create_destroy'

        # Create node with minimum set of parameters
        log.info('Creating vApp %r ...', vapp_name)
        
        node = self.driver.create_node(name=vapp_name, image=image)
        log.info('Completed vApp creation for %r', vapp_name)
        
        self._check_node(node)
                 
        # Destroy the node
        log.info('Destroying vApp %r ...', vapp_name)
        self.driver.destroy_node(node)
        log.info('Destroyed vApp %r ...', vapp_name)
        
    def test07_reboot_node(self):
        vapp_name = 'phil-test07_reboot'
        
        # Query images
        image = self._get_image()
        
        # Create node with minimum set of parameters
        log.info('Creating vApp %r ...', vapp_name)
        node = self.driver.create_node(name=vapp_name, image=image)
        log.info('Completed vApp creation for %r', vapp_name)

        log.info('Rebooting vApp %r ...', vapp_name)
        self.driver.reboot_node(node)
        log.info('%r vApp rebooted', vapp_name)
         
        # Destroy the node
        log.info('Destroying vApp %r ...', vapp_name)
        self.driver.destroy_node(node)
        log.info('Destroyed vApp %r ...', vapp_name)
                
    def test08_create_and_destroy_node_with_ex_network(self):
        # Create with explicit network
        
        # Query images
        image = self._get_image()

        # Create node with specific network setting
        network_r = self.__class__.NETWORK_NAME
        log.info('Creating vApp %r with network %r ...', image, network_r)
        try:
            node = self.driver.create_node(name='phil-test08-node-ex-network', 
                                           image=image,
                                           ex_vm_network='Net-Test',
                                           ex_vm_fence='bridged',
                                           ex_network=network_r)
        except Exception as e:
            self.fail(e)
            
        log.info('Completed vApp creation for %r', node.name)
        
        self._check_node(node)
         
        # Destroy the node
        log.info('Destroying vApp %r ...', image.name)
        self.driver.destroy_node(node)
        log.info('Destroyed vApp %r', image.name)
        
    def test09_create_and_destroy_node_with_ex_vmnames(self):
        # Create with explicit network
        vapp_name = 'phil-test09-ex-vm-name'
        
        image = self._get_image()

        # Create node with specific network setting
        vm_name = 'cust-vm-name01'
        
        log.info('Creating vApp %r with VM name %r ...', image.name, vm_name)
        try:
            node = self.driver.create_node(name=vapp_name, 
                                           image=image,
                                           ex_vm_names=[vm_name])
        except Exception as e:
            self.fail(e.message.attrib)
            
        log.info('Completed %r vApp creation', vapp_name)
        
        self._check_node()
         
        # Destroy the node
        log.info('Destroying vApp %r ...', image.name)
        self.driver.dehstroy_node(node) 
        log.info('Destroyed vApp %r', image.name)
                
    def test10_create_node_adding_execute_script(self):
        
        # Query images
        image = self._get_image()

        ex_script_filepath = self.__class__.EX_SCRIPT_FILEPATH
        
        # Create node with specific network setting
        network_r = self.__class__.NETWORK_NAME
        log.info('Creating vApp %r with network %r ...', image, network_r)
        try:
            node = self.driver.create_node(
                                       name='phil-test10-node-with-ex-script', 
                                       image=image,
                                       ex_vm_network='Net-Test',
                                       ex_vm_fence='bridged',
                                       ex_network=network_r,
                                       ex_vm_script=ex_script_filepath)
        except Exception as e:
            self.fail(e)
            
        log.info('Completed vApp creation for %r', node.name)
        
        self._check_node(node)
         
        # Destroy the node
        log.info('Destroying vApp %r ...', image.name)
        self.driver.destroy_node(node)
        log.info('Destroyed vApp %r', image.name)        
              
if __name__ == "__main__":
    import sys;sys.argv = [
        '', 
        'Vcd55TestCloudClient.test10_create_node_adding_execute_script']
    unittest.main()
