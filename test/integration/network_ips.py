'''
Created on Nov 7, 2014

Integration tests for network.ips module

@author: giacomo
'''
import unittest
from test.test_abstract import ValpaWithNodesAbstractTest
from network.ips import SetsIpAddressesToPhysicalCluster,\
    SetsAddressesToAllPossibleVMs
from network.address import NetworkAddresses
from bean.vm import BuildsAllVMDetails

class SetsIpAddressesToPhysicalClusterTest(ValpaWithNodesAbstractTest):

    def setUp(self):
        super(SetsIpAddressesToPhysicalClusterTest, self).setUp()
        networkAddresses = NetworkAddresses(self.networkingOpts, self.physicalCluster, self.hwSpecs)
        self.ipSetter = SetsIpAddressesToPhysicalCluster(networkAddresses)

    def testSetIpAddresses(self):
        # when
        self.ipSetter.setIpAddresses(self.physicalCluster)
        
        # test ip addresses in physical cluster
        ipAddress1 = self.physicalCluster.getIpAddressOf('node082')
        self.assertEqual(ipAddress1, '172.16.82.254')
        
        ipAddress2 = self.physicalCluster.getIpAddressOf('node083')
        self.assertEqual(ipAddress2, '172.16.83.254')
        
class SetsAddressesToAllPossibleVMsTest(ValpaWithNodesAbstractTest):

    def setUp(self):
        super(SetsAddressesToAllPossibleVMsTest, self).setUp()
        
        self.vmFactory = BuildsAllVMDetails(self.valpaPrefs, self.hwSpecs, self.physicalCluster)
        self.allVMs = self.vmFactory.build()
        
        networkAddresses = NetworkAddresses(self.networkingOpts, self.physicalCluster, self.hwSpecs)
        self.setter = SetsAddressesToAllPossibleVMs(networkAddresses, self.physicalCluster)

    def testSetAddresses(self):
        # when
        self.setter.setAddresses(self.allVMs)
        
        # then
        ipAddress1 = self.allVMs.getIpAddressOf('kvm-pbs082-01')
        macAddress1 = self.allVMs.getMacAddressOf('kvm-pbs082-01')
        
        self.assertEquals(ipAddress1, '172.16.82.1')
        self.assertEquals(macAddress1, '00:16:36:ff:82:01')
        
        ipAddress2 = self.allVMs.getIpAddressOf('kvm-pbs087-12')
        macAddress2 = self.allVMs.getMacAddressOf('kvm-pbs087-12')
        
        self.assertEquals(ipAddress2, '172.16.87.12')
        self.assertEquals(macAddress2, '00:16:36:ff:87:12')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()