'''
Created on Nov 08, 2013

@author: philipkershaw
'''
from os import path
import unittest
import logging
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

from libcloud import security
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

HERE_DIR = path.dirname(__file__)
CONFIG_DIR = path.join(HERE_DIR, 'config')
CA_CERTS_PATH = path.join(CONFIG_DIR, 'ca', 'mozilla-ca-bundle.crt')
CREDS_FILEPATH = path.join(CONFIG_DIR, 'aws_creds.txt')


@unittest.skip("Pending AWS account")
class TestAwsCloudClient(unittest.TestCase):
    
    security.CA_CERTS_PATH = [CA_CERTS_PATH]
    
    def setUp(self):
        USERNAME, PASSWORD = open(CREDS_FILEPATH).read().split(':')
        aws_driver = get_driver(Provider.EC2)
        self.conn = aws_driver(USERNAME, PASSWORD)
        
    def test01_list_nodes(self):
        nodes = self.conn.list_nodes()
        for node in nodes:
            self.assert_(node)
            log.info('node = %r', node)


@unittest.skip("Pending AWS account")
class TestEuWestAwsCloudClient(unittest.TestCase):
    
    security.CA_CERTS_PATH = [CA_CERTS_PATH]
    
    def setUp(self):
        USERNAME, PASSWORD = open(CREDS_FILEPATH).read().split(':')
        aws_driver = get_driver(Provider.EC2_EU_WEST)
        self.conn = aws_driver(USERNAME, PASSWORD)
        
    def test01_list_nodes(self):
        nodes = self.conn.list_nodes()
        for node in nodes:
            self.assert_(node)
            log.info('node = %r', node)               
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
