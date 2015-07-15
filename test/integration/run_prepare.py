'''
Created on Oct 31, 2013

Unit tests for run.prepare

@author: giacomo
'''

import unittest
from run.prepare import PreparesExperiment
from test.test_abstract import VespaDeploymentAbstractTest

class PreparesExperimentTest(VespaDeploymentAbstractTest):
    
    def setUp(self):
        super(PreparesExperimentTest, self).setUp()
        self.prepsExperiment = PreparesExperiment(False, self.vespaPrefs, self.runOpts)
        
    def testPrepare(self):
        # when
        (execConfig, experimentPath) = self.prepsExperiment.prepare(self.clusterRequest, self.deploymentInfo, self.appRequest)
        
        # then
        self.maxDiff = None
        self.assertEquals(execConfig, '/tmp/vespa/execs/446bf85f-b4ba-459b-8e04-60394fc00d5c')
        self.assertEquals(open(execConfig, 'r').read(), open('resources/execConfig-expected.output', 'r').read())
        
        self.assertEquals(experimentPath, '/home/giacomo2/shared/execs/parpac/nc16-cpv4-idf8-psBAL_ONE/a8adc50779f75c6b36fa9c95ddb7fa8a5033df6791235f727a20b0e3e6780e93')
        
if __name__ == '__main__':
    unittest.main()