'''
Created on Jul 11, 2015

@author: giacomo
'''

import unittest

from unit.test_abstract import VespaAbstractTest
from core.simple_specs import SimpleTopologySpecification, SimpleMappingSpecification,\
    SimpleClusterPlacementSpecification
from core.cluster import Topology, Mapping
from core.enum import PinningOpt


class SimpleTopologySpecificationTest(VespaAbstractTest):
    """Unit tests for core.simple_specs.SimpleTopologySpecification. """
    
    def setUp(self):
        VespaAbstractTest.setUp(self)
        self.topologySpec = SimpleTopologySpecification(self.hwSpecs)
        
    def testIsSatisfiedBy1(self):
        topologyRequest = Topology(24, 6)
        self.assertTrue(self.topologySpec.isSatisfiedBy(topologyRequest))
        
    def testIsSatisfiedBy2(self):
        topologyRequest = Topology(25, 6)
        self.assertFalse(self.topologySpec.isSatisfiedBy(topologyRequest))
        
    def testIsSatisfiedBy3(self):
        topologyRequest = Topology(48, 24)
        self.assertFalse(self.topologySpec.isSatisfiedBy(topologyRequest))
        
class SimpleMappingSpecificationTest(VespaAbstractTest):
    """Unit tests for core.simple_specs.SimpleMappingSpecification. """
    
    def setUp(self):
        VespaAbstractTest.setUp(self)
        self.mappingSpec = SimpleMappingSpecification(self.hwSpecs)
        
    def testIsSatisfiedBy1(self):
        mappingRequest = Mapping(6, PinningOpt.BAL_SET)
        self.assertTrue(self.mappingSpec.isSatisfiedBy(mappingRequest))
        
    def testIsSatisfiedBy2(self):
        mappingRequest = Mapping(6, "BAL_SET")
        self.assertTrue(self.mappingSpec.isSatisfiedBy(mappingRequest))
        
    def testIsSatisfiedBy3(self):
        mappingRequest = Mapping(6, "BAL_SAT")
        self.assertFalse(self.mappingSpec.isSatisfiedBy(mappingRequest))
        
    def testIsSatisfiedBy4(self):
        mappingRequest = Mapping(13, PinningOpt.BAL_SET)
        self.assertFalse(self.mappingSpec.isSatisfiedBy(mappingRequest))
        
    def testIsSatisfiedBy5(self):
        # testing valid firstNodeIndex value
        mappingRequest = Mapping(6, "BAL_SET", 3)
        self.assertTrue(self.mappingSpec.isSatisfiedBy(mappingRequest))
        
    def testIsSatisfiedBy6(self):
        # testing invalid firstNodeIndex value
        mappingRequest = Mapping(6, "BAL_SET", 12)
        self.assertFalse(self.mappingSpec.isSatisfiedBy(mappingRequest))
        

class SimpleClusterSpecificationTest(VespaAbstractTest):
    """Unit tests for core.simple_specs.SimpleClusterSpecification. """
    
    def setUp(self):
        VespaAbstractTest.setUp(self)
        self.clusterSpec = SimpleClusterPlacementSpecification(self.hwSpecs)
        
    def testIsSatisfiedBy1(self):
        topologyRequest = Topology(18, 3)
        mappingRequest = Mapping(6, PinningOpt.BAL_SET)
        self.assertTrue(self.clusterSpec.isSatisfiedBy(topologyRequest, mappingRequest))
        
    def testIsSatisfiedBy2(self):
        """ BAL_SET not valid (equals BAL_ONE) """
        topologyRequest = Topology(18, 1)
        mappingRequest = Mapping(6, PinningOpt.BAL_SET) 
        self.assertFalse(self.clusterSpec.isSatisfiedBy(topologyRequest, mappingRequest))
        
    def testIsSatisfiedBy3(self):
        """ idf not valid with topology. """
        topologyRequest = Topology(24, 12)
        mappingRequest = Mapping(6, PinningOpt.BAL_SET) 
        self.assertFalse(self.clusterSpec.isSatisfiedBy(topologyRequest, mappingRequest))
        
    def testIsSatisfiedBy4(self):
        """ Test when firstNodeIndex causes virtual cluster to occupy last nodes """
        topologyRequest = Topology(24, 2)
        mappingRequest = Mapping(6, PinningOpt.NONE, 8) 
        self.assertTrue(self.clusterSpec.isSatisfiedBy(topologyRequest, mappingRequest))
    
    def testIsSatisfiedBy5(self):
        """ Test when firstNodeIndex causes virtual cluster to not fit """
        topologyRequest = Topology(24, 2)
        mappingRequest = Mapping(6, PinningOpt.NONE, 9) 
        self.assertFalse(self.clusterSpec.isSatisfiedBy(topologyRequest, mappingRequest))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()