'''
Created on Oct 14, 2013

Unit tests for deploy.vmgen module

@author: giacomo
'''
import unittest
from unit.test_abstract import VespaDeploymentAbstractTest,\
    VespaInfinibandAbstractTest
from network.address import NetworkAddresses
from create.vm import VMDefinitionDetails, VMDefinitionBasicGenerator,\
    VMXMLSaver

class VMRequestGenerationDetailsTest(VespaDeploymentAbstractTest):
    
    def setUp(self):
        VespaDeploymentAbstractTest.setUp(self)
        networkAddresses = NetworkAddresses(self.networkingOpts, self.physicalCluster, self.hwSpecs)
        self.definitionDetails = VMDefinitionDetails(self.vespaPrefs, networkAddresses) 
        self.definitionDetails.setDeploymentContext(self.deploymentInfo)

    def testGetUUID(self):
        uuidgen = self.definitionDetails.getUUID('kvm-pbs082-01')
        self.assertEqual(len(uuidgen), len('446bf85f-b4ba-459b-8e04-60394fc00d5c'))
        
    def testGetMAC(self):
        mac = self.definitionDetails.getMAC('kvm-pbs082-01')
        self.assertEqual(mac, '00:16:36:ff:82:01')
        
        mac = self.definitionDetails.getMAC('kvm-pbs083-02')
        self.assertEqual(mac, '00:16:36:ff:83:02')

    def testGetVmPath(self):
        path = self.definitionDetails.getVmPath('kvm-pbs082-01')
        self.assertEqual(path, 'node082/kvm-pbs082-01')
        
        path = self.definitionDetails.getVmPath('kvm-pbs083-02')
        self.assertEqual(path, 'node083/kvm-pbs083-02')
        
class VMRequestInfinibandTest(VespaInfinibandAbstractTest):
    
    def setUp(self):
        VespaInfinibandAbstractTest.setUp(self)
        networkAddresses = NetworkAddresses(self.networkingOpts, self.physicalCluster, self.hwSpecs)
        self.definitionDetails = VMDefinitionDetails(self.vespaPrefs, networkAddresses) 
        self.definitionDetails.setDeploymentContext(self.deploymentInfo)
        
    def testGetInfinibandDetails(self):
        slot, vf = self.definitionDetails.getInfiniband('kvm-pbs082-01')
        self.assertEqual(slot, '0x00')
        self.assertEqual(vf, '0x1')
        
        slot, vf = self.definitionDetails.getInfiniband('kvm-pbs082-07')
        self.assertEqual(slot, '0x00')
        self.assertEqual(vf, '0x7')
        
        slot, vf = self.definitionDetails.getInfiniband('kvm-pbs082-08')
        self.assertEqual(slot, '0x01')
        self.assertEqual(vf, '0x0')
        
class BasicVMGenTest(VespaDeploymentAbstractTest):
    
    def setUp(self):
        VespaDeploymentAbstractTest.setUp(self)
        (deployedNodes, deployedSockets, deployedVMs) = self.deploymentInfo  # @UnusedVariable
        networkAddresses = NetworkAddresses(self.networkingOpts, self.physicalCluster, self.hwSpecs)
        definitionDetails = VMDefinitionDetails(self.vespaPrefs, networkAddresses)
        self.basicGen = VMDefinitionBasicGenerator(self.vespaPrefs, definitionDetails)
        self.basicGen.setDeploymentContext(self.deploymentInfo, False)

    def testProduceXMLs(self):
        self.maxDiff = None
        
        xmls = self.basicGen.createDefinitions(self.clusterXML)
        self.assertEqual(type(xmls), type({}))
        
        xml08201 = 'resources/vms/kvm-pbs082-01-basic.xml' 
        self.assertTextEqualsContent(xmls['kvm-pbs082-01'], xml08201)
        
        xml08302 = 'resources/vms/kvm-pbs083-02-basic.xml' 
        self.assertTextEqualsContent(xmls['kvm-pbs083-02'], xml08302)
        
class VmXMLSaverTest(VespaDeploymentAbstractTest):
    '''
    Unit tests for VmXMLSaver
    '''
    
    def setUp(self):
        VespaDeploymentAbstractTest.setUp(self)
        self.xmlDict = {'kvm-pbs082-01' : open('resources/vms/kvm-pbs082-01-balone.xml', 'r').read(),
                          'kvm-pbs082-02' : open('resources/vms/kvm-pbs082-02-balone.xml', 'r').read()}
        
        self.expectedOutput = {'kvm-pbs082-01' : '/tmp/vespa/xmls/testExp/kvm-pbs082-01.xml',
                               'kvm-pbs082-02' : '/tmp/vespa/xmls/testExp/kvm-pbs082-02.xml'}
        
        (deployedNodes, deployedSockets, deployedVMs) = self.deploymentInfo  # @UnusedVariable
        self.xmlSaver = VMXMLSaver(self.vespaPrefs)
        
    def testSaveXMLs(self):
        xmlNameDict = self.xmlSaver.saveXMLs(self.xmlDict, 'testExp')
        
        self.assertEqual(xmlNameDict, self.expectedOutput)
        self.assertTextEqualsContent(self.xmlDict['kvm-pbs082-01'], self.expectedOutput['kvm-pbs082-01'])
        self.assertTextEqualsContent(self.xmlDict['kvm-pbs082-02'], self.expectedOutput['kvm-pbs082-02'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
