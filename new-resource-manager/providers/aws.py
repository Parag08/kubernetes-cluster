from Crypto.PublicKey import RSA
import os
import json
from python_terraform import *
import shutil

templates_folder = './templates/'


def terraformApply(directory):
  tf = Terraform(working_dir=directory)
  return_code, stdout, stderr = tf.init()
  print('init:',return_code,stdout,stderr)
  return_code, stdout, stderr = tf.get()
  print('get:',return_code,stdout,stderr)
  return_code, stdout, stderr = tf.plan()
  print('plan:',return_code,stdout,stderr)
  return_code, stdout, stderr =tf.apply()
  print('apply:',return_code,stdout,stderr)

def cleanDir(directory):
  tf = Terraform(working_dir=directory)
  tf.init()
  return_code, stdout, stderr = tf.destroy('force')
  print('destroy:',return_code,stdout,stderr)
  shutil.rmtree(directory)
  print('cleanup successful')

def createProfile(inputJson,projectFolder):
  outputJson = {}
  try:
    outputJson['provider'] = {"aws": {"access_key": inputJson['resource']['aws'][1]['access_key'],"secret_key": inputJson['resource']['aws'][1]['secret_key'],"region": inputJson['resource']['aws'][1]['region']}}
    outputJson['module'] = {"aws-iam": {"source": "modules/iam","aws_cluster_name": inputJson["basic"]['projectname']}}
    outputJson['resource'] = {"aws_ebs_volume": {"example": {"availability_zone": inputJson['resource']['aws'][1]['region'] + 'a',"size": inputJson['basic']['storage_size'],"type":"gp2"}}}
    with open(projectFolder+'profile_aws'+'/'+'input.tf.json', 'w') as outfile:
      json.dump(outputJson, outfile)
  except Exception as exp:
    print('err in aws/terraformApply:',exp)


def preprocessingProject(inputJson):
  #create project folder
  projectFolder = './project/'+inputJson['basic']['user']+'/'+inputJson['basic']['projectname']+'/'
  try:
    os.makedirs(projectFolder)
  except Exception as exp:
    print('warn in aws/preprocessingProject:',exp)
  #copy terraform templates 
  #1. copy aws profile folder
  try:
    shutil.copytree(templates_folder+'aws'+'/'+'profile_aws',projectFolder + 'profile_aws')
  except Exception as exp:
    print('err in aws/preprocessingProject:',exp,'this is not expected behaviour trying to clean directory and recreating profiles')
    cleanDir(projectFolder + 'profile_aws')
    shutil.copytree(templates_folder+'aws'+'/'+'profile_aws',projectFolder + 'profile_aws')
  #2. create profile input.tf.json
  createProfile(inputJson,projectFolder)
  #3. create profile in aws
  terraformApply(projectFolder+'profile_aws/')
  return projectFolder

def preprocessingInstace(inputJson):
  #create folder for instance and generate key files
  projectFolder = inputJson['projectFolder']
  instancePath = projectFolder + inputJson['label'] + '/'
  inputJson['instancePath'] = instancePath
  try:
    os.makedirs(instancePath)
  except Exception as exp:
    print('warn in aws/preprocessingInstace:',exp)
  key = RSA.generate(2048)
  with open(instancePath+"key", 'w') as content_file:
    content_file.write(key.exportKey('PEM'))
  pubkey = key.publickey()
  with open(instancePath+"key.pub", 'w') as content_file:
    content_file.write(pubkey.exportKey('OpenSSH'))
  #copy output.tf files in folder
  shutil.copy2(templates_folder+'aws'+'/output.tf',instancePath)
  return key.publickey().exportKey('OpenSSH').decode()

def terraformAwsCreate(inputJson):
  #write terraform files
  public_key = preprocessingInstace(inputJson)
  projectName = inputJson['projectName']
  outputJson = {}
  outputJson['provider'] = {"aws": {"access_key": inputJson['access_key'],"secret_key": inputJson['secret_key'],"region": inputJson['region'],"profile": "kubernetes-node"}}
  outputJson['resource'] = {"aws_instance": {"node": {"subnet_id": inputJson['subnet'],"count": 1,"security_groups": [inputJson['security_group']],"ami": inputJson["ami"],"instance_type": inputJson['instance_type'],"iam_instance_profile": "kube_" + projectName + "_master_profile","tags": {"Name": inputJson['label']},"key_name": "${aws_key_pair.deployer.key_name}","root_block_device":{"volume_type": "gp2","volume_size": "300","delete_on_termination": "true"},"provisioner": {"remote-exec": {"inline": ["sudo apt-get update", "sudo apt-get install nfs-kernel-server --yes", "sudo service nfs-kernel-server stop", "sudo apt-get install python --yes","sudo apt-get install ldap-utils --yes"],"connection": {"type": "ssh","user": "ubuntu","private_key": "${file(\"key\")}"}}}}},"aws_key_pair": {"deployer": {"key_name": projectName + inputJson['label'],"public_key": public_key}}}
  with open(inputJson['instancePath']+'input.tf.json', 'w') as outfile:
    json.dump(outputJson, outfile)
  #terraform apply for creating instances
  terraformApply(inputJson['instancePath'])
