""" Unit tests for consolidate.analyzer module. """
import unittest
from consolidate import analyzer
from collections import OrderedDict
from unit.test_abstract import ConsolidateAbstractTest

class AnalyzerTest(ConsolidateAbstractTest):
    
    def setUp(self):
        ConsolidateAbstractTest.setUp(self)
        
        self.parpacInputDir = self.consolidateDir + '/parpac'
        self.timeFilename = 'times.txt'
        
        # given time and application metrics
        timeItems = (('userTime', [227.99, 228.56]),
                     ('systemTime', [16.56, 16.17]),
                     ('ellapsedTime', [122.73, 122.76])
                     )
        appItems = (('appTime', [122.12, 122.2]),
                    ('fluidRate', [3.197, 3.195]),
                    ('floatRate', [1.909, 1.908])
                    )
        self.timeMetrics = OrderedDict(timeItems)
        self.appMetrics = OrderedDict(appItems)
        self.allMetrics = OrderedDict(timeItems + appItems)

    def testGetTimeMetrics(self):
        # given this directory contains parpac-specific metrics
        #User    System    Ellapsed
        #227.99    16.56    122.73
        #User    System    Ellapsed
        #228.56    16.17    122.76 
        configDir = self.parpacInputDir + '/nc4-cpv2-idf0-psBAL_ONE/968f3b98fcab1bc5ae27a8d17a88be0c3a5ff9339b54a958d23957ba51272f9c'

        # when
        timeMetrics = analyzer.getTimeMetrics(configDir, self.timeFilename)
        
        # then keys are exactly in this order
        self.assertEqual(timeMetrics.keys(), ['userTime', 'systemTime', 'ellapsedTime'])
        
        # then content valid
        self.assertEqual(timeMetrics['userTime'], [227.99, 228.56])
        self.assertEqual(timeMetrics['systemTime'], [16.56, 16.17])
        self.assertEqual(timeMetrics['ellapsedTime'], [122.73, 122.76])
        
    def testAreConsistent(self):
        self.assertTrue(analyzer.areConsistent(self.appMetrics, self.timeMetrics))
        
    def testMetricsToCSV(self):
        
        # given output
        metricsFile = '/tmp/vespa-consolidate-analyzer.csv'
        
        # when requesting a CSV
        analyzer.metricsToCSV(metricsFile, self.allMetrics)
        
        # then verify CSV content
        expectedFilename = 'resources/consolidate/consolidate-analyzer.csv'
        self.assertFileContentEqual(metricsFile, expectedFilename)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()