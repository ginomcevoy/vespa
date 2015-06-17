'''
Created on Sep 29, 2014

@author: giacomo
'''
from bean.experiment import Experiment, Scenario
from quik import FileLoader
from autorun.clustergen import SimpleClusterGenerator
from autorun.appgen import AppRequestGenerator

class StandaloneExperimentGenerator():
    '''
    Generates stand-alone experiments (not concurrent) based on 
    cluster and application specifications.
    '''

    def __init__(self, hwSpecs, clusterGenerator, applicationGenerator):
        self.clusterGenerator = clusterGenerator
        self.applicationGenerator = applicationGenerator
    
    def withTechnologies(self, technologyTuple):
        '''
        Optional method to specify VMM technologies
        '''
        self.clusterGenerator.technologyTuple = technologyTuple
        return self
    
    def withTuningOptions(self, tuningTuple):
        '''
        Optional method to specify VMM tunings
        '''
        self.clusterGenerator.tuningTuple = tuningTuple
        return self
    
    def produceScenarios(self, clusterGenSpec, applicationGenSpec):
        '''
        Returns a list of scenario objects based on specifications.
        '''
        scenarios = []
        
        # get all virtual clusters
        clusterRequests = self.clusterGenerator.generateWithSpecification(clusterGenSpec)
        
        # generate application requests, sensitive to virtual cluster specs
        for clusterRequest in clusterRequests:
            appRequests = self.applicationGenerator.generateFor(applicationGenSpec, clusterRequest)
            for appRequest in appRequests:
                experimentName = self.nameForExperiment(clusterRequest, appRequest)
                experiment = Experiment(experimentName, clusterRequest, appRequest, 1)
                scenario = Scenario([experiment, ])
                scenarios.append(scenario)
                
        return scenarios
            
    def nameForExperiment(self, clusterRequest, appRequest):
        return clusterRequest.__str__()
    
class SimpleScenariosToXMLExporter():
    '''
    Exports a list of scenarios to a single XML. Assumes the scenarios are
    stand-alone (no concurrent experiments) and that the cluster requests
    use the simple characterization (DIST tuple)
    '''
    def __init__(self, templateFile = '../templates/builder.template'):
        self.templateFile = templateFile
        
    def exportScenarios(self, scenarios, xmlPath, xmlName):
        
        # text base for template building
        xmlFilename = xmlPath + '/' + xmlName
        xmlFile = open(xmlFilename, 'w')
        xmlText = '<?xml version="1.0"?>\n<scenarios>\n'
        
        for scenario in scenarios:
            experiment = scenario.getExperiment()
            app = experiment.app
            cluster = experiment.cluster
            
            # Use template, with all local variables set
            loader = FileLoader('.')
            template = loader.load_template(self.templateFile)
            text = template.render(locals(), loader=loader)#.decode('utf-8')
            xmlText += text
        
        # close XML file now
        xmlText += '</scenarios>\n'
        xmlFile.write(xmlText)
        xmlFile.close()
        
        return xmlFilename 
        
class SimpleScenarioGenerator():
    '''
    Generates scenarios with stand-alone experiments using the simple
    virtual cluster characterization. Performs all the necessary setup
    so that it is ready to use.
    '''
    
    def __init__(self, hwSpecs, defaultTechnology=None, defaultTuning=None, templateFile = '../templates/builder.template'):
        
        # prepare clusterRequest and applicationRequest generators
        clusterGenerator = SimpleClusterGenerator(hwSpecs, defaultTechnology, defaultTuning)
        applicationGenerator = AppRequestGenerator()
        
        # prepare delegate scenario generator
        self.scenarioGenerator = StandaloneExperimentGenerator(hwSpecs, clusterGenerator, applicationGenerator)
        
        # prepare scenario to XML exporter
        self.toXMLExporter = SimpleScenariosToXMLExporter(templateFile)
        
    def withTechnologies(self, technologyTuple):
        '''
        Optional method to specify VMM technologies
        '''
        self.scenarioGenerator.withTechnologies(technologyTuple)
        return self
    
    def withTuningOptions(self, tuningTuple):
        '''
        Optional method to specify VMM tunings
        '''
        self.scenarioGenerator.withTuningOptions(tuningTuple)
        return self
    
    def withXML(self, xmlPath, xmlName):
        self.xmlPath = xmlPath
        self.xmlName = xmlName
        return self
    
    def withClusterSpecification(self, clusterGenSpec):
        self.clusterGenSpec = clusterGenSpec
        return self
    
    def withApplicationSpecification(self, appGenSpec):
        self.appGenSpec = appGenSpec
        return self
    
    def produceXML(self):
        scenarios = self.scenarioGenerator.produceScenarios(self.clusterGenSpec, self.appGenSpec)
        return self.toXMLExporter.exportScenarios(scenarios, self.xmlPath, self.xmlName)