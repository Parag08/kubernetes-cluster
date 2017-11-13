[![Build Status](https://secure.travis-ci.org/Parag08/kubernetes-cluster.png?branch=master)](http://travis-ci.org/Parag08/kubernetes-cluster) 

# Kubernetes cluster setup

   
A utility to start your own kubernetes cluster with JSON requests   

<b>Architecture</b>
   
```
DB [project-schema] -> UI [generated based on project schema] -> API [backend api] (schema to terraform) 
-> TERRAFORM [start instances] -> KUBESPRAY [create kubernetes] -> API [create services in kubernetes]
```

<b>example</b>
   
kubernetes-cluster/new-resource-magaes/json/input.json   
