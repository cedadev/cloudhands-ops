"""JASMIN Cloud

Cloudhands ops functional tests Azure Apache libcloud tests
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
from libcloud.compute.base import NodeAuthPassword
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


# Location of the directory containing *this* module
HERE_DIR = path.dirname(__file__)

# The configuration directory holds files for setting the vCD hostname and 
# user credentials, also, a CA directory for CA certificate bundle file
CONFIG_DIR = path.join(HERE_DIR, 'config')

# File containing the authentication credentials.  It should be of the form
# <vCloud id>@<vCloud Org Name>:<password>
CREDS_FILEPATH = path.join(CONFIG_DIR, 'creds.txt')

    
@unittest.skip("Site-specific code. To go into cloudhands-jasmin.")
class AzureTestCloudClient(unittest.TestCase):
    '''Test Azure against Apache Libcloud 
    '''
    SUBSCRIPTION_ID = open(CREDS_FILEPATH).read().strip()
    KEY_FILEPATH = path.join(CONFIG_DIR, 'azure-management.cer')
    
    # Pick image name from environment variable or accept default
    IMAGE_NAME = environ.get('TEST_CLOUD_CLIENT_IMAGE_NAME') or \
'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04-LTS-amd64-server-20140606.1-en-us-30GB'
    
    CLOUD_SERVICE_NAME = 'ubuntu1404t8'
    
    # Disable SSL verification for testing ONLY
#    security.CA_CERTS_PATH = [CA_CERTS_PATH]
    security.VERIFY_SSL_CERT = False
    
    def setUp(self):
        driver = get_driver(Provider.AZURE)
        self.driver = driver(subscription_id=self.__class__.SUBSCRIPTION_ID, 
                             key_file=self.__class__.KEY_FILEPATH)

    def _get_image(self):
        '''Query for images and return set by class var'''
        images = self.driver.list_images()

        for image in images:
            if image.id == self.__class__.IMAGE_NAME:
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
        
    def test02_list_nodes(self):
        nodes = self.driver.list_nodes(
                        ex_cloud_service_name=self.__class__.CLOUD_SERVICE_NAME)
        self.assert_(nodes)
        for node in nodes:
            self.assert_(node)
            log.info(node)
        
    def test03_list_images(self):
        # List all available image templates
        images = self.driver.list_images()
        log.info('Images ...')
        for image in images:
            self.assert_(image)
            log.info(image)

    def test04_list_locations(self):
        locations = self.driver.list_locations() 
        
        self.assert_(locations, 'No locations returned')
        
        for loc in locations: 
            for attr, val in loc.__dict__.items(): 
                if not attr.startswith('_'):
                    log.info("%r=%r" % (attr, val))
                
            log.info('='*80)
                            
    def test05_create_and_destroy_node(self):
        # Query images
        image = self._get_image()

        appl_name = 'philtest05' # won't accept '-' '_' symbols?

        # Create node with minimum set of parameters
        log.info('Creating vApp %r ...', appl_name)
        
        # FIXME: fudge for now - the image arg should be type NodeImage 
        node = self.driver.create_node(
                       name=appl_name, 
                       image=image.id, 
                       size='Medium',
                       auth=NodeAuthPassword("Pa55w0rd", False),
                       ex_cloud_service_name=self.__class__.CLOUD_SERVICE_NAME,
                       ex_storage_service_name=self.__class__.CLOUD_SERVICE_NAME,
                       ex_deployment_name="deployment_name",
                       ex_deployment_slot="Production",
                       ex_admin_user_id="azure")

        log.info('Completed vApp creation for %r', appl_name)
        
        self._check_node(node)
                 
        # Destroy the node
        log.info('Destroying vApp %r ...', vapp_name)
        self.driver.destroy_node(node)
        log.info('Destroyed vApp %r ...', vapp_name)
        
              
if __name__ == "__main__":
    import sys;sys.argv = [
        '', 
        'AzureTestCloudClient.test05_create_and destroy_node']
    unittest.main()
