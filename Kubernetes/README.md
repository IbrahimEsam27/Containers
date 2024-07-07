# Kubernetes
**Container orchestration service (platform)**

- [Kubernetes](#kubernetes)
  - [High Level Architecture of Kubernetes](#high-level-architecture-of-kubernetes)
  - [Installation](#installation)
    - [Install Minikube](#install-minikube)
  - [Architecture of Kubernetes](#architecture-of-kubernetes)
    - [Differences between Containers (Orchestration native like docke swarm) and Kubernetes](#differences-between-containers-orchestration-native-like-docke-swarm-and-kubernetes)
  - [Sample Deployment](#sample-deployment)
  - [Steps](#steps)
    - [1- Create Deployment](#1--create-deployment)
  - [](#)
    - [2- Create Service](#2--create-service)
    - [3- Deployment Scaling](#3--deployment-scaling)
    - [4- Update](#4--update)
  - [Minikube Dashboard](#minikube-dashboard)



## High Level Architecture of Kubernetes
*We have (**manager**) nodes and (**worker**) nodes*

**Inside (Manager nodes) we have some components:**
 - **API Server** == (docker deamon [docker engine])
>Kubernetes has more than Interface 
> - **CLI** : kubectl
> - **DashBoard**: GUI
> - **API Interface**: for example: python or java modules --> talk with kubernates with **Restful APIs**
> - **curl**
 - **etcd** : database has all configurations of the cluster, it hav key value store for every thing(saved in memory , Highly available , Replicable)
 - **schedulers** : Component that creats deployment , modify in replias set.
 - **Controller manager**: Compare between current state of cluster and its components and the desired state (between the current configurations and those ones in etcd).
 - **Cloud Controller manager** (optional)

**Inside (worker nodes) we have some components:**
components that response to the control plane:
 - **kubelet**: responsible on 
    - It's the agent talks with manager
    - Executes scheduler tasks
    - Reports the statues of node to the manager
- **kubeproxy**: Manage anything related to the network
---
## Installation
 - Kubernetes can be installed on (data centers, pyhsical machine , virtual machine , multi node , in a Cloud(Native or on VMs)..) and this is for production
 - There is another installation for test and Dev ---> Put all components **(Control plane , Worker Nodes)** in the same area.
 - Manager nodes of Kubernetes (available for linux only) , Workers (MCS or Linux)
 - The Installation is done by **Minikube**
 - When Installing Minikube --> I can all Componenets of Kubernetes in a Container or Virtual machine that have all Componenets **(Control plane , Worker Nodes)**
> Note: Kubernetes is not a Container run time **(like docker which creates containers nativly)**,, Kubernetes uses Container run time **(like docker , runc , LXC )** to create containers
### Install Minikube
 - Install Minikube
```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```
 - Install kube CTL (for managing the cluster)
```sh
snap install kubectl --classic
```
 - Make suer that they have been installed
```sh
minikube version
kubectl version 
```
 - Install on virtual machine
```sh
#for Virtual machine
minikube start --vm-driver virtualbox --cpus 2 --memory 4096

#For docker 
minikube start --driver docker --cpus 2 --memory 4096
```
 - Go to Virtualbox to make sure that your VM has been created
![](https://i.imgur.com/sruSeD5.png)
> *Got Some message when Installation recommend to use qemu*
```sh
    You have selected "virtualbox" driver, but there are better options !                          
    For better performance and support consider using a different driver:                          
            - qemu2                                                                                
    To turn off this warning run:                                                                  
            $ minikube config set WantVirtualBoxDriverWarning false                                
    To learn more about on minikube drivers checkout https://minikube.sigs.k8s.io/docs/drivers/    
    To see benchmarks checkout https://minikube.sigs.k8s.io/docs/benchmarks/cpuusage/
```
 - Check that minikube running
```sh
minikube status
```
and
```sh
kubectl cluster-info
```
*We get the IP of the cluster **``https://192.168.59.100:8443``***
 - Open minikube Dashboard **``minikube dashboard``**
 - We can get the nodes with **``kubectl get nodes -o wide``**
---
## Architecture of Kubernetes
The most three Important We use Kubernetes for: **(High Availabitily, Scalabilty, Disaster ecovery)**
 - **High Availabitily**: Application is always upon running regaldless Containers shut down or not , we do (replica set).
 - **Scalabilty**: Tolerate the Load , Load balancing on many containers.
 - **Disaster recovery**: If Smthing bad happned, It recover fastly.
### Differences between Containers (Orchestration native like docke swarm) and Kubernetes
 - Every Container has its IP , if the container died so when the container rstarts it takes new IP so It's a big problem ,, So we need a better way
 - The base of Kubernetes is not the Container, But Something called **pod** , this is many containers together ,  so when we talk about the IP address we consider IP address of the pod not  a single container
>**Pod** considerd as an **Abstraction layer** (for container or more) , so When we do deployment we deploy **Pod** not a single container (we might define specs of container), replicas also made at level of **Pod**
 - End-user deal with something called Deployment (this is more than pod)
>**Note**: Service is group of containers , Deployment is group of pods
 - At level of deployment we determine the (repilca set and update methods)
 - After Deployment we determine the **replication**
 - Above Deployment level there is a **Service** level and this is layer which user Interacts with ,,, and this is for Load balancing so that the user doesn't deal with deployment 
 - We can say that the service is a **Load balancer**, it decide which avaliable node and deployment which has less load , it distributes the load
 - We can make one layer above the service (Ingress network) , this is for naming of url instead of ``node1.service:port.com`` to ``myapp.com`` so it translates that url to that simple one
 - We have persistance volume for all deployment , let's take an example if i have database in my voulume called postgress and I want to replace it with DB called mysql so should we change that name in all connections and pods?? the answer is no
 - we use object called **Config map** it's just a configuration in the config.file to change to make all ex: **my_db** ->> this is the data base which all pods looks at , so when i cahnge my my_db in the config.file from postgrass to mysql ---- the problem is done
 - so we understand that we're trying to abstaract everything to reduce dependenies , I don't put every configs together (Secrets , name , IP , names of Env var ... etc)
---
## Sample Deployment
![](https://i.imgur.com/RmgpNt8.png)
```sh
#Get ip of the cluster
minikube ip
#192.168.59.100
```
---
## Steps
### 1- Create Deployment
```sh
kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1
# --image --> for containers inside pods
#Output will be (deployment.apps/kubernetes-bootcamp created) on terminal
```
 - Check Changes
```sh
kubectl get all
```
 - WE got three things
    - ``pod/kubernetes-bootcamp-644c5687f4-pqg5x`` (this is a created pod)
    - ``service/kubernetes`` (this is a created Service)
    - ``deployment.apps/kubernetes-bootcamp`` (this is the same name I created for the deployment)
    - ``replicaset.apps/kubernetes-bootcamp-644c5687f4`` (This is a created replica set)
 - to See Configs inside pods
```sh
kubectl get pod #get name of pod with id ex:kubernetes-bootcamp-644c5687f4-pqg5x
curl http://localhost:8001/api/v1/namespaces/default/pods/kubernetes-bootcamp-644c5687f4-pqg5x
#Access API server for the control plane
```
>**Note**: to get path of any pod in **etcd** DataBase , path of every component in Kubernetes is located in: http://localhost:8001/api/namespaces/default/pods/kubernetes-bootcamp-644c5687f4-pqg5x
> the default name space is **default** unless I defined I create deployment in specific name space
 - The result is faild **WHY??** Because the way to access anything related to Network we must start kubeproxy first
```sh
kubectl proxy
#get Starting to serve on 127.0.0.1:8001 , it works on port 8001
```
 - In another terminal we try again ``curl http://localhost:8001/api/namespace/default/pods/kubernetes-bootcamp-644c5687f4-pqg5x``, will give us Congigs of the pod (like Inspect)
 - The next Step after creating deployment and pod ----> Create Service 
> **Note**: Service is Expose (-p host port:docker port),,, In Kubernetes we can't open deploment directly , we create service which Access deployment ``kubectl expose deployment`` it's considered as mapping to the port and this is considered a service
> 
> **Note**: Like Containers can do exec to execute command inside the pod
>  
> ``kubectl ecex <name of the pod> --env`` for example to get all env variables
> 
> ``kubelctl logs <name of pod>`` to get logs
>
> Like Containers ``kubectl exec -it <pod name> -- bash`` to attach a shell inside the pod
![](https://i.imgur.com/SUa2lNX.png)
---
### 2- Create Service
 - Check what services we have
```sh
kubectl get services
#create service to access deployment with it
kubectl expose deployment.apps/kubernetes-bootcamp --type="NodePort" --port 8080 
#service/kubernetes-bootcamp exposed
```
>--type="NodePort" : means that k8s will choose the port it exposes the deployment to.
 - Now we found new service created
```sh
kubectl get services
#NAME                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
#kubernetes-bootcamp   NodePort    10.109.226.246   <none>        8080:30244/TCP   2m22s
#it chose port 30244
```
 - To get info about any service
```sh
kubectl describe service/kubernetes-bootcamp
```
 - To access the service we need 
    - IP of the cluster ``minikube ip``
    - port exposed ``kubectl describe service/kubernetes-bootcamp``
```sh
curl $(minikube ip):30244
#Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-644c5687f4-pqg5x | v=1
```
 - If we checked ``kubectl get all`` we find that we have 1 Deploymnt , 1 pod , 1 replac set and 2 services
---
### 3- Deployment Scaling
 - To have Many deployments not one only and every deployment have more than pod
```sh
kubectl scale deployment.apps/kubernetes-bootcamp --replicas=4
#deployment.apps/kubernetes-bootcamp scaled
kubectl get deployments
#NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
#kubernetes-bootcamp   4/4     4            4           78m
```
 - Now we jave 4 deployments and also 4 pods
```sh
kubectl get pods
#NAME                                   READY   STATUS    RESTARTS   AGE
#kubernetes-bootcamp-644c5687f4-m82ls   1/1     Running   0          80s
#kubernetes-bootcamp-644c5687f4-ndjz2   1/1     Running   0          80s
#kubernetes-bootcamp-644c5687f4-pqg5x   1/1     Running   0          79m
#kubernetes-bootcamp-644c5687f4-tmwlx   1/1     Running   0          80s
```
>Now if we do the same command  **``curl $(minikube ip):30244``**
and get message *(Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-644c5687f4-pqg5x | v=1)* , 
>
>This is curl on IP of the cluster itself and the port we created in that service,, **BUT** I don't tell him to go to which deployment I tell him I want that service ,, and the service will distrubute the request or see which deployment is available it depend of Intellegnece of kube proxy and Scheduler itself (seee which one is available and go there)
 - Every time I will do same command It's expected thar different pod to response
```sh
curl $(minikube ip):30244
#Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-644c5687f4-pqg5x | v=1
curl $(minikube ip):30244
#Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-644c5687f4-ndjz2 | v=1
```
 - Kubernetes uses docker runtime to create containers
```sh
kubectl get nodes -o wide
#NAME       STATUS   ROLES           AGE     VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE              KERNEL-VERSION   CONTAINER-RUNTIME
#minikube   Ready    control-plane   4h15m   v1.30.0   192.168.59.100   <none>        Buildroot 2023.02.9   5.10.207         docker://26.0
```
---
### 4- Update
 - Get Image Version of the pods
```sh
kubectl describe pods
#Image:          gcr.io/google-samples/kubernetes-bootcamp:v1
```
 - Update with new version
```sh
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
#deployment.apps/kubernetes-bootcamp image updated
```
 - To do rollout for all deployments
```sh
kubectl rollout status deployments/kubernetes-bootcamp
#deployment "kubernetes-bootcamp" successfully rolled out
```
 - Check Image has been changed
```sh
kubectl describe pods
#Image:          jocatalin/kubernetes-bootcamp:v2
```
---
## Minikube Dashboard
![](https://i.imgur.com/A24CkA3.png)
 - In **Deployment** Section we have option to Edit resource and this is yml or json file that have all configurations which most of it done by K8s , I can Modify what I want from that file
![](https://i.imgur.com/KXygiSY.png) 
 - The same in **Service** Section and Pod and all Componenets

**So We Conclude that Mostly we can just Modify Configurations file to make our work done**
 - To delete our work we can use the following
```sh
kubectl delete deployments --all 
#deployment.apps "kubernetes-bootcamp" deleted
kubectl delete services --all 
#service "kubernetes" deleted
#service "kubernetes-bootcamp" deleted
kubectl delete pods --all 
#pod "kubernetes-bootcamp-5475b47cd4-65cpk" deleted
#pod "kubernetes-bootcamp-5475b47cd4-6rkc4" deleted
#pod "kubernetes-bootcamp-5475b47cd4-lrp9p" deleted
#pod "kubernetes-bootcamp-5475b47cd4-n7ltc" deleted
```
 - Check 
```sh
kubectl get all
#NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
#service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   83s
```
 - Create all the previous with .yml file
```sh
kubectl apply -f k8s.yml
```
---
