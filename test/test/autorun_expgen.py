'''
Created on Nov 10, 2013

@author: giacomo
'''
import unittest
from autorun.expgen import NPBExecutableGenerator, ExperimentGenerator
from bean.experiment import Application, AppTuning  # @UnusedImport
from bean.enum import PinningOpt

class ExperimentGeneratorTest(unittest.TestCase):


    def setUp(self):
        self.hwSpecs = {'cores' : 12, 'sockets' : 2}
        self.expGen = ExperimentGenerator(self.hwSpecs)
        
        self.allCpvs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

    def testWithCpvValues(self):
        # given
        cpvs = (5, 6, 12,)
        
        # when
        self.expGen.withCpvValues(cpvs)
        
        # then
        self.assertEquals(self.expGen.idfs, {'5' : (5, 10), '6' : (6, 12), '12' : (12,)})
        
    def testWithMachines1(self):
        # given
        cpvs = (12,)
        machineTuple = (1,)
        
        # when
        self.expGen.withCpvValues(cpvs)
        self.expGen.withMachines(machineTuple)
        
        # then
        #print(self.expGen.combinations)
        self.assertEquals(self.expGen.combinations, [(12, 12, 0),])
        
    def testWithMachines2(self):
        # given
        cpvs = (1, 12,)
        machineTuple = (1, 2)
        
        # when
        self.expGen.withCpvValues(cpvs)
        self.expGen.withMachines(machineTuple)
        
        # then
        #print(self.expGen.combinations)
        self.assertEquals(self.expGen.combinations, [(1, 1, 0), (2, 1, 0), (3, 1, 0), (4, 1, 0), (5, 1, 0), (6, 1, 0), (7, 1, 0), (8, 1, 0), (9, 1, 0), (10, 1, 0), (11, 1, 0), (12, 1, 0), (12, 12, 0), (2, 1, 1), (4, 1, 2), (6, 1, 3), (8, 1, 4), (10, 1, 5), (12, 1, 6), (14, 1, 7), (16, 1, 8), (18, 1, 9), (20, 1, 10), (22, 1, 11), (24, 1, 12), (24, 12, 12)])
        
    def testWithMachines3(self):
        # given
        cpvs = (1, 2, 4, 6, 8, 12,)
        machineTuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        
        # when
        self.expGen.withCpvValues(cpvs)
        self.expGen.withMachines(machineTuple)
        
        # then
        self.assertEquals(len(self.expGen.combinations), 300)
        
        # verify integrity of tuples
        for experiment in self.expGen.combinations:
            self.assertEquals(experiment[0] % experiment[1], 0) # nc / cpv = #vms
            self.assertEquals(experiment[2] % experiment[1], 0) # idf / cpv = #vmsPerHost)
            if experiment[2] == 0:
                self.assertTrue(experiment[0] <= self.hwSpecs['cores']) # one machine
            else:
                self.assertTrue(experiment[0] / experiment[2] <= 12) # many machines
                
        # grouped combinations
        groups = self.expGen.groups
        #print(groups)
        self.assertEquals(len(groups.keys()), 31) # will be 31 XMLs
        
    def testGenerateXML1(self):
        
        # given 
        appInfo = Application('npb-ep', 10, '')
        experimentList = [(1, 1, 0), (2, 1, 0)]
        self.expGen.withPstratValues((PinningOpt.BAL_ONE, PinningOpt.NONE))
        self.expGen.withPinCores()
        xmlPath = '../output/autorun/generated' 
        
        #print(os.path.abspath(os.path.curdir))
        
        # when
        xmlName = self.expGen.generateXML(experimentList, appInfo, xmlPath)
        
        # then
        self.maxDiff = None
        self.assertEquals(xmlName, '../output/autorun/generated/npb-ep-cpv1-idf0.xml')
        self.assertEquals(open(xmlName, 'r').read(), open('resources/generated1.xml', 'r').read())
        
    def testGenerateXMLs(self):
        
        # given 
        appInfo = Application('npb-ep', 10, '')
        self.expGen.withCpvValues((6, 12))
        self.expGen.withMachines((1, 2, 3))
        self.expGen.withPstratValues()
        self.expGen.withPinCores()
        xmlPath = '../src/autorun/generated' 
        
        # when
        xmlNames = self.expGen.generateXMLs(appInfo, xmlPath)
        
        # then
        if False:
            print(xmlNames)
        
class NPBExecutableGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.hwSpecs = {'cores' : 12, 'sockets' : 2}
        self.execGen = NPBExecutableGenerator(self.hwSpecs)
        
        self.allCpvs = (1, 2, 4, 6, 8, 12)

    def testProduceCoreSet(self):
        # given
        cpvs = (3, 4,)
        maxMachines = 2  # up to 24 cores
        
        # when
        coreSet = self.execGen.produceCoreSet(cpvs, maxMachines)
        
        # then
        self.assertEquals(coreSet, {3, 4, 6, 8, 9, 12, 16, 18, 24})

            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()