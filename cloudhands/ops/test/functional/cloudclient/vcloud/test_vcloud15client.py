"""JASMIN Cloud

Cloudhands ops functional tests vCloud 1.5 Apache libcloud tests
"""
__author__ = "P J Kershaw"
__date__ = "25/01/14"
__copyright__ = "(C) 2014 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__revision__ = "$Id$"
from os import path
import unittest
from urllib.request import urlopen
import logging
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

from libcloud import security
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

HERE_DIR = path.dirname(__file__)
CONFIG_DIR = path.join(HERE_DIR, 'config')
CA_CERTS_PATH = path.join(CONFIG_DIR, 'ca', 'ca-bundle.crt')
CREDS_FILEPATH = path.join(CONFIG_DIR, 'creds.txt')
CLOUD_HOSTNAME_FILEPATH = path.join(CONFIG_DIR, 'cloud-host.txt')


@unittest.skip("Sunsetting vDirector 1.5")
class Vcd15TestCloudClient(unittest.TestCase):
    USERNAME, PASSWORD = open(CREDS_FILEPATH).read().split(':')
    CLOUD_HOSTNAME = open(CLOUD_HOSTNAME_FILEPATH).read().strip()
    
    security.CA_CERTS_PATH = [CA_CERTS_PATH]
    
    IMAGE_NAME = 'Routed-Centos6.4a'
    
    def setUp(self):
        
        vcloud_driver = get_driver(Provider.VCLOUD)
        self.conn = vcloud_driver(self.__class__.USERNAME,
                                  self.__class__.PASSWORD, 
                                  host=self.__class__.CLOUD_HOSTNAME,
                                  port=443,
                                  api_version='1.5')
        
    def test01_check_ca_bundle(self):
        self.assert_(security.CA_CERTS_PATH, 'No CA bundle set')
        log.info(security.CA_CERTS_PATH)
                
    def test02_list_vdcs(self):
        vdcs = self.conn.vdcs
        self.assert_(vdcs)
        
        for i in vdcs:
            log.info("vDC ID: %r", i.id)
            log.info("vDC Name: %r", i.name)
            log.info("vDC Driver: %r", i.driver)
            log.info("vDC Storage: %r", i.storage)
            log.info("vDC Memory: %r", i.memory)
            log.info("vDC CPU: %r", i.cpu)
        
    def test03_list_nodes(self):
        nodes = self.conn.list_nodes()
        self.assert_(nodes)
        for node in nodes:
            self.assert_(node)
            log.info(node)
        
    def test04_list_images(self):
        # List all available vApp Templates
        images = self.conn.list_images()
        log.info('Images ...')
        for image in images:
            self.assert_(image)
            log.info(image)

    def test05_list_locations(self):
        locations = self.conn.list_locations()
        self.assert_(locations, 'No locations returned')
        
    def test05a_get_networks(self):
        networks = self.conn.networks
        for network in networks:
            log.info('network: %r, %r' % (network.attrib['name'], 
                                          network.attrib['href']))
            
            # Check network status
            network_fp = urlopen(network.attrib['href'])
            log.info("network content %r", network_fp.read())
        
    def test06_create_and_destroy_node(self):
        # Query images
        images = self.conn.list_images()

        # Create node with minimum set of parameters
        log.info('Creating vApp ...')
        node = self.conn.create_node(name='Phil-Test-Node01', image=images[0])
        log.info('Completed vApp creation')
        
        nodes = self.conn.list_nodes()
        self.assert_(nodes)
        for node in nodes:
            self.assert_(node)
            log.info(node)
         
        # Destroy the node
        self.conn.destroy_node(node)
        
    def test07_reboot_node(self):
        images = self.conn.list_images()

        # Create node with minimum set of parameters
        log.info('Creating vApp ...')
        node = self.conn.create_node(name='Phil-Test-Node02', image=images[-1])
        log.info('Completed vApp creation')

        log.info('Rebooting vApp ...')
        self.conn.reboot_node(node)
        log.info('Node rebooted')
                
    def test08_create_and_destroy_node_with_ex_network(self):
        # Create with explicit network
        
        # Query images
        images = self.conn.list_images()

        image_found = False
        for image in images:
            if image.name == self.__class__.IMAGE_NAME:
                image_found = True
                break
            
        if not image_found:
            self.fail('No %r image found in list of images available: %r' % 
                      (self.__class__.IMAGE_NAME, images))

        # Create node with specific network setting
        network_r = 'CEMSTEST ORG-EXT-R'
        
        log.info('Creating vApp %r with network %r ...', image, network_r)
        try:
            node = self.conn.create_node(name='phil-test-node-ex-network01', 
                                         image=image,
                                         ex_network=network_r)
        except Exception as e:
            self.fail(e)
            
        log.info('Completed vApp creation')
        
        nodes = self.conn.list_nodes()
        self.assert_(nodes)
        for node in nodes:
            self.assert_(node)
            log.info(node)
         
        # Destroy the node
        log.info('Destroying vApp %r ...', image.name)
        self.conn.destroy_node(node)
        
    def test09_create_and_destroy_node_with_ex_vmnames(self):
        # Create with explicit network
        vapp_name = 'phil-test-node-ex-vm-name01'
        
        # Query images
        images = self.conn.list_images()

        image_found = False
        for image in images:
            if image.name == self.__class__.IMAGE_NAME:
                image_found = True
                break
            
        if not image_found:
            self.fail('No %r image found in list of images available: %r' % 
                      (self.__class__.IMAGE_NAME, images))

        # Create node with specific network setting
        vm_name = 'cust-vm-name01'
        
        log.info('Creating vApp %r with VM name %r ...', image.name, vm_name)
        try:
            node = self.conn.create_node(name=vapp_name, 
                                         image=image,
                                         ex_vm_names=[vm_name])
        except Exception as e:
            self.fail(e)
            
        log.info('Completed %r vApp creation', vapp_name)
        
        nodes = self.conn.list_nodes()
        self.assert_(nodes)
        for node in nodes:
            self.assert_(node)
            log.info(node)
         
        # Destroy the node
        log.info('Destroying vApp %r ...', image.name)
        self.conn.destroy_node(node) 
        
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
