'''
Created on Nov 2, 2014

@author: giacomo
'''
import unittest

from core.physical import PhysicalNodeFactory
from unit.test_abstract import VespaAbstractTest


class PhysicalNodeFactoryTest(VespaAbstractTest):

    def setUp(self):
        VespaAbstractTest.setUp(self)
        self.nodeFactory = PhysicalNodeFactory(self.hwInfo)
        self.subsetNames = ('node084', 'node086', 'node088') 

    def testGetAllNodes(self):
        allNodes = self.nodeFactory.getAllNodes()

        self.failIf(allNodes is None)
        self.assertEqual(len(allNodes.nodeTuple), 12, 'wrong length nodes')
        self.assertEqual(allNodes.getNames()[0], 'node082', 'wrong first node')
        self.assertEqual(allNodes.getNames()[11], 'node093', 'wrong last node')

        self.assertEqual(allNodes.getNodeSuffix('node083'), '083', 'wrong node')
        self.assertEqual(allNodes.getNodeSuffix('node093'), '093', 'wrong last node')
        
        self.assertEqual(allNodes.getNodeIndex('node083'), 1, 'wrong indexing')
        self.assertEqual(allNodes.getNodeIndex('node093'), 11, 'wrong indexing')
        
    def testGetSubset(self):
        # given
        allNodes = self.nodeFactory.getAllNodes()
        
        # when select a subset
        nodeSubset = allNodes.getSubset(self.subsetNames)
        
        # the
        self.assertEqual(len(nodeSubset.getNames()), 3, 'wrong size') 
        self.assertEqual(nodeSubset.getNodeIndex('node084'), 2, 'wrong indexing')
        self.assertEqual(nodeSubset.getNodeIndex('node086'), 4, 'wrong indexing')
        self.assertEqual(nodeSubset.getNodeIndex('node088'), 6, 'wrong indexing')
        
    def testToFile(self):
        # given 
        allNodes = self.nodeFactory.getAllNodes()
        filename = '/tmp/vespa-allnodes.txt'
        
        # when representing as file
        allNodes.toFile(filename)
        
        # verify content
        self.assertFileContentEqual(filename, 'resources/nodes-tofile-expected.txt')
        
    def testFindNumberSuffix(self):
        nodeName = 'node083'
        suffix = self.nodeFactory.findNumberSuffix(nodeName)
        self.assertEqual(suffix, '083')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()