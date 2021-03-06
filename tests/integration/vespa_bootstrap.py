'''
Created on Nov 7, 2014

Integration tests for bootstrap module. VespaWithBootstrapAbstractTest
serves as a base unit for other integration tests that use the bootstrap.

@author: giacomo
'''
import difflib
import unittest

import bootstrap
from create.runner import ExperimentSetRunner
import warnings

class VespaWithBootstrapAbstractTest(unittest.TestCase):

    def setUp(self):
        forReal = False # only simulate VM definitions/instantiations
        vespaFilename = 'resources/vespa.params'
        hardwareFilename = 'resources/hardware.params'
        templateDir = 'resources'
        masterTemplate = 'master.xml'
        inventoryFilename = 'resources/vespa.nodes'
        bootstrap.doBootstrap(forReal, templateDir, masterTemplate, 
                              vespaFilename, hardwareFilename, inventoryFilename)
        self.bootstrap = bootstrap.getInstance()
        (self.vespaPrefs, self.vespaXMLOpts, self.runOpts, self.networkingOpts, self.repoOpts) = self.bootstrap.getAllConfig()
        
    def assertMultiLineEqual(self, first, second, msg=None):
        '''
        Assert that two multi-line strings are equal.
        If they aren't, show a nice diff.
        '''
        isStringFirst = isinstance(first, str) or isinstance(first, unicode)
        isStringSecond = isinstance(second, str) or isinstance(second, unicode)
        self.assertTrue(isStringFirst,
                'First argument is not a string')
        self.assertTrue(isStringSecond,
                'Second argument is not a string')

        if first != second:
            message = ''.join(difflib.ndiff(first.splitlines(True),
                                                second.splitlines(True)))
            if msg:
                message += " : " + msg
            self.fail("Multi-line strings are unequal:\n" + message)
        
class BootstrapNetworkingTest(VespaWithBootstrapAbstractTest):
    
    def setUp(self):
        VespaWithBootstrapAbstractTest.setUp(self)
        
    def testVMNetworking(self):
        allVMDetails = self.bootstrap.getAllVMDetails()
        
        ipAddress = allVMDetails.getVM('kvm-pbs086-11').getIpAddress()
        self.assertEquals(ipAddress, '172.16.86.11')
        
        macAddress = allVMDetails.getVM('kvm-pbs093-04').getMacAddress()
        self.assertEquals(macAddress, '00:16:36:ff:93:04')
        
    def testGetExperimentSetRunner(self):
        
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            
            # Use the bootstrapper to get the experiment runner:
            # this will activate the application configurator and trigger a warning
            # for invalid configuration ('invalid' folder)
            runner = self.bootstrap.getExperimentSetRunner()
            
            # then verify warning
            assert len(w) == 1
            assert issubclass(w[-1].category, SyntaxWarning)
            assert "Bad application.config" in str(w[-1].message)
            
        # verify target instance
        self.assertTrue(isinstance(runner, ExperimentSetRunner))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()