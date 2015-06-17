'''
Created on Oct 13, 2013

@author: giacomo
'''
import unittest

from config import valpaconfig

class ValpaConfigBase (unittest.TestCase):

    def setUp(self):
        self.expectedValpaPrefs = {'master_vm' : 'ubuntu14.04-node',
                                   'vm_pernode' : '12', 
                                   'vm_prefix' : 'kvm-pbs',
                                   'vm_pattern' : '&PREFIX&NODESUFFIX-&VMSUFFIX',
                                   'vm_mem_base' : '0', 
                                   'vm_mem_core' : '1024', 
                                   'vm_mac_base' : '00:16:36:ff',
                                   'vm_xml_output' : '/tmp/valpa/xmls',
                                   'exec_config_template' : '../templates/execConfig.template',
                                   'exec_config_output' : '/tmp/valpa/execs',
                                   'general_verbose' : '1',
                                   'xml_cluster_path' : 'vms'}

        self.expectedXMLOpts = {'xml_disk_drivertype' : 'raw', 
                                'xml_disk_path' : '/home/giacomo2',
                                'xml_disk_file' : 'disk.img',
                                'xml_disk_dev' : 'vda'}
        
        self.networkingOpts = {'network_source' : 'external-bridge',
                               'net_name_bridge_use' : 'valpa-external-bridge',
                               'net_name_bridge_create' : 'valpa-libvirt-bridge',
                               'net_name_sriov' : 'valpa-sriov'}

    def testValpaConfig(self):
        valpaFile = 'resources/valpa.params'
        valpaCfg = valpaconfig.readValpaConfig(valpaFile)

        # valpaPrefs
        valpaPrefs = valpaCfg.getValpaPrefs()
        self.failIf(type(valpaPrefs) != type({}))
        self.maxDiff = None
        self.failUnlessEqual(valpaPrefs, self.expectedValpaPrefs)

        # valpaXMLOpts
        valpaXMLOpts = valpaCfg.getValpaXMLOpts()
        self.failIf(type(valpaXMLOpts) != type({}))
        self.failUnlessEqual(valpaXMLOpts, self.expectedXMLOpts)

    def testMasterXML(self):
        valpaXML = valpaconfig.produceValpaXML(self.expectedXMLOpts, self.networkingOpts, 'resources/master.xml')

        # compare with expected output
        self.maxDiff = None
        expectedValpaXML = open('resources/valpa-expected.xml', 'r').read()
        self.failUnlessEqual(valpaXML, expectedValpaXML)
    
# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(ValpaConfigTest())
#     suite.addTest(ValpaMasterXMLTest())
#     return suite
# 
if __name__ == '__main__':
    unittest.main()
    # runner = unittest.TextTestRunner()
    # runner.run(suite())

