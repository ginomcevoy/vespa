'''
Created on Jun 23, 2015

@author: giacomo
'''
import unittest
from unit.test_abstract import VespaWithNodesAbstractTest


class TestPhysicalCluster(VespaWithNodesAbstractTest):
    '''
    Integration test for PhysicalCluster that uses the bootstrapper 
    to create an Ansible inventory for the physical nodes.
    '''
    def setUp(self):
        VespaWithNodesAbstractTest.setUp(self)
        self.inventoryFilename = '/tmp/vespa-node-inventory.test'
    
    def testCreateInventory(self):
        # when
        self.physicalCluster.createInventory(self.inventoryFilename, self.allVMDetails)
        
        # then get expected content in the inventory file
        actualContent = open(self.inventoryFilename, 'r').read()
        expectedContent = open('resources/inventory-node-expected.txt', 'r').read()
        self.assertMultiLineEqual(actualContent, expectedContent, 'Node inventory')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()