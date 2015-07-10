'''
Created on Oct 13, 2013

@author: giacomo
'''

import unittest
from test.test_abstract import VespaAbstractTest

class GetHardwareInfoTest(VespaAbstractTest):
    
    def setUp(self):
        super(GetHardwareInfoTest, self).setUp()

    def testHardwareInfo(self):

        # hardware
        specs = self.hwSpecs
        self.failUnlessEqual(specs['cores'], 12, 'cores wrong')
        self.failUnlessEqual(specs['sockets'], 2, 'sockets wrong')
        self.failUnlessEqual(specs['mem'], 24, 'mem wrong')

        # nodes
        hwInfo = self.hwInfo
        self.failUnlessEqual(hwInfo.nodePrefix, 'node', 'prefix wrong')
        self.failUnlessEqual(hwInfo.nodeZeros, 3, 'nodeZeros wrong')
        self.failUnlessEqual(hwInfo.nodeFirst, 82, 'nodeFirst wrong')
        
    def testReadInventoryFile(self):
        nodeNames = self.nodeNames
        self.assertEqual(12, len(nodeNames))
        self.assertEqual('node082', nodeNames[0])
        self.assertEqual('node093', nodeNames[11])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()