'''
Created on Nov 2, 2014

@author: giacomo
'''
import unittest
from test.test_abstract import ValpaWithNodesAbstractTest
from bean.vm import BuildsAllVMDetails, VirtualClusterFactory

class BuildsAllVMDetailsTest(ValpaWithNodesAbstractTest):

    def setUp(self):
        super(BuildsAllVMDetailsTest, self).setUp()
        self.vmFactory = BuildsAllVMDetails(self.valpaPrefs, self.hwSpecs, self.physicalCluster)

    def testGetAllNodes(self):
        allVMDetails = self.vmFactory.build()

        self.failIf(allVMDetails is None)
        self.failUnlessEqual(len(allVMDetails.vmDict.keys()), 72, 'wrong amount of VMs')
        
        vmsInFirstNode = allVMDetails.byNode['node082']
        self.failUnlessEqual(vmsInFirstNode[0], 'kvm-pbs082-01')
        self.failUnlessEqual(vmsInFirstNode[11], 'kvm-pbs082-12')

        vmsInLastNode = allVMDetails.byNode['node087']
        self.failUnlessEqual(vmsInLastNode[5], 'kvm-pbs087-06')
                
        allNames = allVMDetails.getNames()
        self.failUnlessEqual(len(allNames), 72)
        
        aVMIndex = allVMDetails.getVMIndex('kvm-pbs084-02')
        self.failUnlessEqual(aVMIndex, 1)
        
        aVMNumber = allVMDetails.getVMNumber('kvm-pbs085-12')
        self.failUnlessEqual(aVMNumber, 12)
        
        aVMSuffix = allVMDetails.getVMSuffix('kvm-pbs086-08')
        self.failUnlessEqual(aVMSuffix, '08')
        
class AllVMDetailsTest(ValpaWithNodesAbstractTest):
    
    def setUp(self):
        super(AllVMDetailsTest, self).setUp()
        self.vmFactory = BuildsAllVMDetails(self.valpaPrefs, self.hwSpecs, self.physicalCluster)
        self.allVMDetails = self.vmFactory.build()
        
    def testGetSubset(self):
        # Choose according to nc=6, cpv=1, idf=2
        vmNames = ('kvm-pbs082-01', 'kvm-pbs082-02',
                   'kvm-pbs083-01', 'kvm-pbs083-02',
                   'kvm-pbs084-01', 'kvm-pbs084-02',)
        subsetDetails = self.allVMDetails.getSubset(vmNames)
        
        # then
        vmDictKeys = subsetDetails.vmDict.keys()
        self.assertEquals(len(vmDictKeys), 6)
        self.assertEquals(sorted(vmDictKeys), sorted(vmNames))
        self.assertEquals(subsetDetails.getHostingNode('kvm-pbs082-02'), 'node082')
        
        byNodeKeys = subsetDetails.byNode.keys()
        self.assertEquals(len(byNodeKeys), 3)
        self.assertEquals(sorted(byNodeKeys), sorted(('node082', 'node083', 'node084')))
        self.assertEquals(sorted(subsetDetails.byNode['node084']), sorted(('kvm-pbs084-01', 'kvm-pbs084-02')))

class VirtualClusterFactoryTest(ValpaWithNodesAbstractTest):

    def setUp(self):
        super(VirtualClusterFactoryTest, self).setUp()
        vmDetailsFactory = BuildsAllVMDetails(self.valpaPrefs, self.hwSpecs, self.physicalCluster)
        allVMDetails = vmDetailsFactory.build()
        self.vmTemplateFactory = VirtualClusterFactory(allVMDetails)
        
    def testCreate(self):
        # given VMs according to nc=6, cpv=2, idf=4
        vmNames = ('kvm-pbs082-01', 'kvm-pbs082-02',
                   'kvm-pbs083-01', 'kvm-pbs083-02',
                   'kvm-pbs084-01', 'kvm-pbs084-02',)
        cpv = 2
        
        # when
        clusterTemplate = self.vmTemplateFactory.create(vmNames, cpv)
        
        # then
        self.failIf(clusterTemplate is None)
        self.failUnlessEqual(len(clusterTemplate.vmDict.keys()), 6, 'wrong amount of VMs')
        
        vmsInFirstNode = clusterTemplate.byNode['node082']
        self.failUnlessEqual(vmsInFirstNode[0], 'kvm-pbs082-01')
        self.failUnlessEqual(vmsInFirstNode[1], 'kvm-pbs082-02')

        vmsInLastNode = clusterTemplate.byNode['node084']
        self.failUnlessEqual(vmsInLastNode[1], 'kvm-pbs084-02')
                
        allNames = clusterTemplate.getNames()
        self.failUnlessEqual(sorted(allNames), sorted(vmNames))
        
        aVMIndex = clusterTemplate.getVMIndex('kvm-pbs084-02')
        self.failUnlessEqual(aVMIndex, 1)
        
        aVMNumber = clusterTemplate.getVMNumber('kvm-pbs083-02')
        self.failUnlessEqual(aVMNumber, 2)
        
        aVMSuffix = clusterTemplate.getVMSuffix('kvm-pbs082-01')
        self.failUnlessEqual(aVMSuffix, '01')
        
        aCpv = clusterTemplate.getCpv('kvm-pbs084-01')
        self.failUnlessEqual(aCpv, 2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()