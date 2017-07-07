import sys
import os
import logging
#sys.stdout = open('deploy.log','w+')

class deploy:
    terraformDict = {}
    def __init__(self,projectDict,awsDict,instanceDict):
        self.projectDict = projectDict
        self.awsDict = awsDict
        self.instanceDict = instanceDict
        self.cwd = os.getcwd()
        
    def createProjectFolder(self):
        ''' 
        create project folder and subfolders also copies necessary files
        '''
        logging.info('utility:createProjectFolder project folders being created')
        projectName = self.projectDict.projectname
        userName = self.projectDict.projectname
        directory = self.cwd + userName
        if not os.path.exists(directory):
            os.makedirs(directory)
        directory = directory + '/' + projectName
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.projectFolder = directory
        logging.info('utility:createProjectFolder project folder creation sucessful projectfolder:'+projectFolder)

    def createTerraformTemplates(self):
        '''
        creates terraformTemplates from aws 
        '''
        logging.info('utility:createTerraformTemplates creating terraform templates')
        instances = self.instanceDict['instances']
        for instance in instances:
            logging.info('creating templates for instance:'+instance.name)
            template = {}
            template['provider'] = {"aws":{"access_key":self.awsDict["access_key"]}}
            
        
    def writeTerraformTemplates(self):
        '''
        '''
    def getStatus(self):
        '''
        '''
