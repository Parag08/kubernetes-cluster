import json
import providers.aws as aws
import os

mapping_folder = './json/'
project_folder = './project/'

if __name__ == "__main__":
  with open(mapping_folder+'input.json') as data_file:
    data = json.load(data_file)

def imageSelector(provider,imageNames,os,selector):
  try:
    filename = provider+'-'+imageNames+'-'+os+'-'+'mapping.json'
    path = mapping_folder + filename
    print("selecting ami from:",path)
    with open(path) as data_file:
      mapping = json.load(data_file)
      return mapping[selector]
  except Exception as exp:
    print('error:',exp)

def createCluster(inputjson):
  for provider in inputjson['resource']:
    if provider == 'aws':
      inputjson['projectFolder'] = aws.preprocessingProject(inputjson)
      for instance in inputjson['resource']['aws']:
        instance['projectName'] = inputjson['basic']['projectname']
        instance['projectFolder'] = inputjson['projectFolder']
        instance['ami'] = imageSelector('aws','ami',inputjson['basic']['os_type'],instance['region'])
        aws.terraformAwsCreate(instance)

def deleteCluster(inputJson):
  projectFolder = project_folder+inputJson['basic']['user']+'/'+inputJson['basic']['projectname']+'/'
  folders =  [d for d in os.listdir(projectFolder) if os.path.isdir(os.path.join(projectFolder, d))]
  for folder in folders:
    aws.cleanDir(projectFolder+folder)

#createCluster(data)
deleteCluster(data)
