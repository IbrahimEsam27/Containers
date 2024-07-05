# Docker

- [Docker](#docker)
  - [Docker Commands](#docker-commands)
    - [Example working with hadoop](#example-working-with-hadoop)
    - [Stopping containers gracefully](#stopping-containers-gracefully)
    - [Self-healing containers with restart policies](#self-healing-containers-with-restart-policies)
    - [Copy file from Host to Inside Container](#copy-file-from-host-to-inside-container)
  - [Networking in Containers](#networking-in-containers)
    - [Three types of Networks in containers (Bridge , Host, Null(None))](#three-types-of-networks-in-containers-bridge--host-nullnone)
    - [Network Drivers](#network-drivers)
    - [Create Network](#create-network)
  - [Storage in Docker](#storage-in-docker)
  - [Containerizing an Application](#containerizing-an-application)
    - [Make an image for me from that Container](#make-an-image-for-me-from-that-container)
  - [Dockerfile](#dockerfile)
    - [Image Registry](#image-registry)
  - [docker-compose](#docker-compose)
    - [Conter-app using docker-compose](#conter-app-using-docker-compose)
  - [Docker Swarm](#docker-swarm)
  - [Docker Stack](#docker-stack)
      - [Weakness in docker swarm](#weakness-in-docker-swarm)
  - [Portainer](#portainer)
## Docker Commands
```bash
docker pull alpine:latest
docker create --name my_alpine_container alpine:latest /bin/sh
docker start -i my_alpine_container # (i) to be interactive
```
 - Use the following will do the same three commands in one command
```bash
docker run -it alpine:latest /bin/sh -c "apk update && apk add bash && bash"
```
 - To download from un-official source on docker.hub you should use
```bash
docker container run -it --name "hadoopc" -h hadoopc asami76/hadoop-pseudo:v1.0 bash -c "/usr/local/bootstrap.sh ;bash"
```
 - **(-it)** to open interactive terminal , we can use (-d) if it's a web service or run in background
 - **(--name)** to name my container because if i don't, the engine choose random names for my container
 - **(-h)** to name my os in the host
 - **(asami76/hadoop-pseudo:v1.0)** this is the repo name and this is how to write the image in case it's not official source [owner of repo/reponame:tag of repo]
 - **(-c "/usr/local/bootstrap.sh ;bash")** this is to start that scripts when opening the container, and it's common use with complex applications in containers, we run some script and it will handle other things
---
### Example working with hadoop
 - Inside container
```bash
ip addr show #to see the ip of container and by default it starts with 172
```
 - Got to an browser and write ``http://172.17.0.2:9870`` and now it's open and you can do any ops
 - You can create dir in hadoop from browser and it's reflected in localhost Container
```bash
hdfs dfs -ls hdfs://localhost:9000 #you will see dir i created on hadoop
```
 - You can create dir in container and it will be reflected on hadoop 
```bash
hdfs dfs -mkdir hdfs://localhost:9000/testuserhdfs #you will see dir i created on localhost
```
 - Be careful when exiting the container : any dir i created wil be deleted
 - Knowing Info about the image, it will give json file have info about the image
```bash
docker image inspect b48 #b48 is first 3 letters in ID
```
 - The same for container
```bash
docker container inspect c7e #c7e is the first three digits in container id
```
 - To remove all Images and its all layers
```bash
docker image rm $(docker image ls -q) # (-q) shows the id of containers
```
---
### Stopping containers gracefully
docker container stop sends a SIGTERM signal to PID(1)
If the process doesn't exit in 10 sec it sends a SIGKILL signal
### Self-healing containers with restart policies
Restart policies are applied per-container, and can be configured imperatively on the command line as part of docker container run commands, or declaratively in YAML files for use with higher-level tools

 - **always**
container will always restart if the main process is killed from inside the container but won't restart if you manually stopped it. Will restart if the Docker daemon restarts.
 - **unless-stopped**
container will always restart if the main process is killed from inside the container but won't restart if you manually stopped it. However will NOT restart if the Docker daemon restarts.
 - **on-failue**
container will always restart if the main process exits with non-zero code (i.e. with error) but won't restart if you manually stopped it. However will restart if the Docker daemon restarts.

``docker container run --name <container-name> --restart always <image-name> <process>``
```bash
$ docker container run --name neversaydie -it --restart always alpine sh
# exit
$ docker container ls
$ docker container inspect neversaydie
```
check the RestartCount item in the inspection json.

---
### Copy file from Host to Inside Container
```bash
#In Host Machine
touch file.py
docker container cp ./file.py 1ff:/tmp/file.p # (1ff) is the first 3 digits in container name
```
```python
#Inside Python Container
import os
os.listdir('/tmp')
#['file.py']
exec(open('/tmp/file.py').read())
#Hello from Python Container
```
## Networking in Containers
 - You can create simple Container based on nginx 
```bash
docker container run -d --name web nginx:latest
```
> You can get **ip** of that container with ``inspect`` command , Ip is **172.17.0.2**
 - **Now,** you can create another Container based on simple image like alpine or centos
```bash
docker container run -it --name client centos:latest
```
 - We can talk between two containers with ip
```bash
#inside Client Container (Centos)
ping 172.17.0.2 #The ip of Web Application (nginx Container)
curl http://172.17.0.2 #Get Message from Nginx <title>Welcome to nginx!</title>
```
 - we can inside host files : create name of the container and its ip of the onther container
```bash
docker container run -it --name client --add-host web:172.17.0.2 centos:latest
```
 - **Every Creating Container will create virtual network adabtor on the host**
```bash
ip link show #on the host
```
**EX:** 
```
56: veth813197d@if55: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default 
    link/ether ca:3c:a9:72:0a:5d brd ff:ff:ff:ff:ff:ff link-netnsid 1
```
### Three types of Networks in containers (Bridge , Host, Null(None))
 - The Default is Bridge
 - Creating with None network (Null Driver: Ex: I creted VM without any network)
```bash
docker container run -it --name alp3 --network none alpine:latest 
```
it will be isolated from outside, when using ``ifconfig`` inside container, we find ``lo`` only and there is no ``eth0`` or ``en0``, but when using bridge network it will appear
 - Network ``host``: it will claim (Simulate) Host and it's a special case not common use , In this Case there is no need for port Forwarding (Port mapping)
```bash
docker container run -d --name web --network host nginx
```
### Network Drivers
The Single Host has by default 3 types of drivers
 - Bridge (Most common)
 - Macvlan
 - Overlay (For Multiple User)
### Create Network

```sh
docker network create mynet # Default Bridge
docker network ls #will find the Three main Networks (Bridge, Host, None) + my new network and by default Bridge driver
```
 - Connect Network to a container >docker network connect < Name of my network > < Name of Container >

```sh
docker network connect mynet alp1
```
 - Define Subnet when creating
```sh
docker network create --subnet 1.0.0.0/16 mynet2
```
 - To disconnect Container from the Network
```sh
docker network disconnect mynet2 alp2 
```
 - After Disconnection if tried to ping ip of one container from the other, it cannot done

 - **``--internal``** --> This makes the network intrnal only, the containers on same network can talk to each other but can't talk or ping the outsiders [Internal is a switch to make the bridge Network but can't talk to Internet] ---> we can use it for testing Env Variable
```sh
docker network create --internal mynet3
docker network connect mynet3 alp1
docker network connect mynet3 alp2
## Inside alp1
ping 172.19.0.2 #will ping on alp2
ping 8.8.8.8 #will not ping because it's internal
```
---
## Storage in Docker
 - during Existince of the container in the host (Running or Stopped), it will take a space to put its files in 
```sh
sudo -s #Because this is a previlage dir can't access with normal user
cd /var/lib/docker
ls
```
 - You find the following directories and we want directory overlay2 (This is the driver for the Storage)

``buildkit  containers  engine-id  image  network  overlay2  plugins  runtimes  swarm  tmp  volumes``

 - Inside Overlay2 and before creating any images you will just find dir called (l) it's a system folder doesn't matter
 - After pulling an image there will be a layer of that image and this is the (Read/write) Layer that Container inherit when running and inside that layer you can find ``diff`` directory that has file system like any linux os
```sh
cd overlay2 && ls
#310f11c5a42d6350c49c22f91fa33b9e5ad0c8dfa8dd13493cd72582da3414c8
cd 310f11c5a42d6350c49c22f91fa33b9e5ad0c8dfa8dd13493cd72582da3414c8
cd diff && ls 
```
 - After Creating any Container from that image, you find that two new directories has been created in **overlay2** and those belong to the container, inside the **``container directory/diff``** it's still empty, but when running the container and creating any file inside, it wil be reflected in **``container directory/diff``**
```sh
#Inside running container
touch /tmp/my_file
#Inside Host in (container directory/diff)
cd /var/lib/docker/overlay2/bfb70b2fc42fd1862e02648b16a649e1a72868f3881116b4e9ef06c50d327841/diff
ls
#will find (tmp) directory
cd /tmp && ls
## will find (my_file) i created from inside the container
``` 
 - so will find that **``diff``** directory inside the container directory, will have any change i do inside the container itself
 - When Stopping the container (Not DELETING), The files is still exist inside the diff directory on host
 - When Removing the Container, the directory inside Overlay2 which belongs to the container will be deleted and our data the same **SO WHAT IS THE SOLUTION??**
 - one of Methodes We Do **Bind Mounting**, when creating the container, I order some Space in my host to be Mounted or shared inside the container
```bash
docker container run -it -v /home/ibrahim/DevOps/Containers/Docker/code:/app/code python:latest
```
 - Inside My Python Container
```py
import os 
os.listdir('/app/code')
#will List the files i created on the host
exec(open('/app/code/file.py').read())
#prints "Hello from Python Container"
```
- Now if I Changed any thing in my python file on the host, it wil be reflected immedietly inside the container, and if I deleted The container, the space in my host whil not be affected 

 - **Second Method**: CREATE VOLUME and find it in **``/var/lib/docker/volumes``**
```sh
docker volume create myvol
docker container run -it -v myvol:/app/code python bash
```
 - when adding any file inside  **myvol**, Specificly in **``/var/lib/docker/volumes/myvol/_data``**, it will be reflected immedeitly inside the container in **``/app/code``**
 - We can use The same volume to more than one Container
---
## Containerizing an Application
 - Start my container (Python) to run flusk framework
```sh
#Inside Host
docker container run -it --name pyflusk python bash
#Inside Container
mkdir app
```
>**Note**: will try to use vim but, the images are minimal as much as can be, so we have to install vim, **BUT** System repos are usually not update so we have to update and upgrade before installation
```sh
apt update
apt upgrade
apt install vim
```
 - Now we have vim and can create files
 - Create Simple Flask App 
```sh
pip install flask
cd /app
vim hello.py
```
 - **Flask App**
```py
from flask import Flask
app = Flask(__name__)
# the minimal Flask application
@app.route('/')
def helloworld():
    return 'Flask Hello World!'
@app.route('/Hema_ELgamed')
def test():
    return 'A7la Mesa 3lek ya Bro'
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=5000)
```
### Make an image for me from that Container 
```bash
docker commit pyflusk ibrahimesam170/pyflask:v1.0 
#(pyflusk) is my container name and (ibrahimesam170/pyflask:v1.0) is name of the image
```
 - Now i can create new Container from that image by Following:
```bash
docker container run -d -p 5000:5000 --name pyf ibrahimesam170/pyflask:v1.0 python /app/hello.py
```
---
## Dockerfile
 - write Dockerfile
```Dockerfile
FROM python:latest
#Creating dir and cd 
WORKDIR /app
COPY requirments.txt .
RUN pip install -r requirments.txt
COPY hello.py .
EXPOSE 5000
#This will be executed during runtime of the container
CMD python app/hello.py
```
 - Build Image giving the tag version
```sh
docker build -t ibrahimesam170/pyflask:v1.1 .
```
 - Create container from that image we built
```sh
docker container run -d --name pyflask -p 5000:5000 ibrahimesam170/pyflask:v1.1
```
 - Now If we wanted to Modify anything inside our application, we can just build a new version of the dockker image with one command
```sh
#After Modifing the application Giving it Tag V1.2
docker build -t ibrahimesam170/pyflask:v1.2 .
docker container run -d --name pyflask -p 5000:5000 ibrahimesam170/pyflask:v1.2
```
 - Some Commands
```Dockerfile
#FROM 
#FROM --> Inherit the Env var of the base image been called
FROM python
FROM ibrahimesam170/pyflask:v1.1

#ADD
ADD <url> /app
ADD <tar archieve> /app

#SHELL
#This means consider any command you will execute in Dockerfile during build time is /bin/bash not default /bin/sh , if i wnt to RUN command that needs bash, so must out /bin/bash before RUN
SHELL ["/bin/bash" , "-c"] 
SHELL ["/usr/local/bin/python" , "-c"]

#RUN
#SHELL MODE
RUN <command> <arg1> <arg2>
#EXEC MODE 
RUN ["command" , "arg1" , "arg2"]

#metadata
#ENV -->for Enviroment variables used during build time,(#FROM --> Inherit the Env var of the base image been called),Env Var inside the layers of image
ENV <name> <value>
ENV PATH $PATH:/app

#LABEL --> doesn't affect
LABEL maintainer = "Ibrahim Esam"
LABEL Description = "This is Docker Container"

#USER --> by default the user is root inside container, many images don't have option to change user (su - <username>), so we can add group and user and switch to that user
RUN groupadd my_group && useradd -g my_group my_user
USER my_user
RUN id

#ENTRYPOINT
ENTRYPOINT ["/bin/bash" , "-c"]

#CMD
CMD [<Arguments of Entry point>]

#ARG -->within scope of Dockerfile (inside docker file not the image like ENV)
ARG <arg>=<value>
ARG PYTHON_IMAGE_NAME=python
```
---
### Image Registry
 - Upload my image on docker.hub
```bash
docker tag <old name of image in my host> <name appear in repo>
#The name must be name of my account/name of image:tag
docker tag pyflask ibrahimesam170/pyflask:v1.1

#Push Image
docker image push ibrahimesam170/pyflask:v1.1
```
> **Notes**
> 
> 1- when pushing image have many tags, if didn't specify tag, all images will be pushed.
> 
> 2- when pushing new image or version, docker hub will see if any similar layes in the repos, so you won't upload all layers abnd this is Good way of **Optimization**
---
## docker-compose
 - Service is more than container + network + storage
 - we can conisder every service is devided to many microservices and we can consider evey microservice is a container so we want to get them together
 - docker-compose Automates creation of services
 - Installation 
```bash
sudo curl -L https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
#We can check version of docker-compose
docker-compose --version
```
### Conter-app using docker-compose
 - create docker-compose.yml
```yml
version: "3.7"
services:
  web-fe:
    build: .
    command: python app.py
    ports:
      - target: 5000
        published: 5000
    networks:
      - counter-net
    volumes:
      - type: volume
        source: counter-vol
        target: /code
  redis:
    image: "redis:alpine"
    networks:
      counter-net:

networks: #This key tells dicker engine to create network called counter-net
  counter-net: #this is equivelent to (docker network create counter-net)

volumes:
  counter-vol: #this is equivelent to (docker volume create counter-vol)
```
 - I have my app.py and my Dockerfile in the same directory,**NOW** i will execute docker-compose proccess
```bash
docker-compose up & #if the default name (docker-compose.yml)
#docker-compose up -f <any other name> &
```
> Note: Every component created by dpcker-compose **(Image - Container - Network - Storage)** will have the name of the application (directory name) before its name, **EX**: (**Network**:counter-app_counter-net ,**Volume**:counter-app_counter-vol ,**Image**:counter-app_web-fe , **Containers**:counter-app-web-fe-1, counter-app-redis-1 )
 - We can override the defaults by setting Keys in docker-compose.yml file bu setting **``container name:``**
> **Note**: 
> Containers can talk to each other with name of the service or name of container (on the same Network)
>
> **EX**: from web-fe container **``ping redis``** I can ping the other services like redis

 - One way of testing
```bash
docker exec<id of container> ping -c 1 google.com
# OR Test Each other
docker exec 849 ping -c 2 redis
#OR 
docker-compose exec <name of srvice> ping -c 2 <name of another service>
```
 - **Deleting Services (Deleting Containers)**
```sh
docker-compose down
```
> This will delete all services, so delete all containers , Networks ,**BUT** don't delete Images or Volumes
---
## Docker Swarm
 - As we have too much containers, so we will need a new hosts for our containers, so Docker swarm helps in clustering docker host and orechestration for the services for that swarm

```bash
#Address of my machine and port of docker swarm 2377
docker swarm init --advertise-addr 192.168.1.14:2377 --listen-addr 192.168.1.14:2377
```
 - we get on terminal
```bash
Swarm initialized: current node (smlbs204wuj4oj7z62y0o15ui) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-23oe6p5ssnhg56hcgpur976qjnrdnw9z99wr2brturwtniiiko-77xa1ktzf82vl6ufssun99zzi 192.168.1.14:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```
 - The token we get is used by any worker to join the swarm and to get the token from simple command
```sh
docker swarm join-token worker
```
 - To add a manager to the swarm 
```sh
docker swarm join-token manager
```
 - we should prepare our hosts (**Ex**: 5 VM-machines)
 - When write the previous command we get a command with token in the terminal, we Copy this command the worker command in worker hosts (nodes) , and managers as well
```sh
#Example of manager command
docker swarm join --token SWMTKN-1-23oe6p5ssnhg56hcgpur976qjnrdnw9z99wr2brturwtniiiko-a1wfiirfoe8t2vnpzu5le8ydq 192.168.1.14:2377
```
> we must have number of managers == (1 or 3 or 5 or 7) only

 - After that we can check with **``docker node ls``**, and we'll find number of nodes and type if leader , manager, worker

> Note: Standlone Container on the one host (one of the nodes), the swarm doesn't care about it, it must be created by service (belongs to the swarm)

 - Service Deployment in Swarm
```sh
docker service create --name web -p 80:80 --replicase 5 nginx:latest
```
> **--replicase** : number of containers in that service

 - After executing the previous command i will get a message on terminal ``verify: Service pen6tqwck115wwy9787dtz6ao converged `` (service converged means that all containers are built and ready) ,AND crete new two networks (**ingress**: overlay driver , **docker_gwbrige**: bridge) , AND distribute the containers to my nodes

> Note: **``docker service ps web``** to see all containers and how ther are distributed between VMs

 - To remove the service from Swarm , and now there is no services
```sh
docker service rm web
```
 - Let's try to make 2 replicas only , IN my case i was making 2 VMs as worker and 3 VMs as a manager, so what i got is :: replicants created in workers only and in my host the Leader doesn't have the container
 - But when trying to access **``http://localhost:80``** from my main (leader VM) , it's able to **HOW???** ; This is Because of **(ingress) network** which is shared between hosts, the docker swarm forwarded the port from one host to another
 - If wanna to change number of replicas in service
```sh
docker service scale web=9
```
and now we will find that hosts may have more than replicas

 - **``dockersamples/visualizer``** is an image open web interface shows how docker swarm is
```sh
docker service create \
  --name=viz \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer
```
 - Go to **``http://localhost:8080``** and you see a visualization of docker swarm
> Note: in the previous service the container was restarting itself even when i tried to rm the container by force, and tried to kil the process which using the port 8080,,, but the solution is to remove the service itself and in our case use **``docker service rm viz``** and if the service didn't been removed we can scale it down to 0 **``docker service scale viz=0``** then **``docker service rm viz``** and then make sure that the service has been removed **``docker service ls``**

 - **IMPORTANT NOTE:** If one host (node) is out of service because of any reason (Ex: failure or **``sudo service docker stop``**) , The default that the services will be disturbuted over other nodes and you can check by **``docker node ls``** and **``docker service ps web``** and find that there is shutdown nodes , BUT when that host returns back to work **``sudo service docker start``**, the services doesn't come back by default (It's configurable) , **``docker node ls``** will find that the node is Active , **BUT** **``docker service ps web``** the services were belong to it in past are still with other hosts

 - Update Service (in my example using nginx image V1.21 and  want latest Version)
```sh
docker service update --image nginx:latest --update-parallelism 2 --update-delay 5s web
```
> **--update-parallelism 2** : means that you update every two containers together
>
> **--update-delay 5s** : wait 5 seconds after every update
>
> The old Containers are still exist but **STOPPED**

 - **IMPORTANT NOTE:** we created service from nginx image easily without any problems, But if tried to do the same with ubuntu image it will fail **WHY??**
```bash
docker service create --name ubuntu_serv --replicas 2 ubuntu:latest #It FAILS
```
> We must have a service running not just stand alone container with no service running, so in case of ubuntu there is no service running
>
> Every service have a desired state (every service is stateful not like container) , so when a service been terminated in on of its components it tries to restart again to reach the desired state, in the example above the service want 6 replicas so when happened that one or more nodes has been shutdown **What happened?** the service run on other nodes , so we understand that any service will try to reach its desired state , **In ubunut service there is no desired state no running service**
 - If I wanted to run ubuntu **what should we do??** ,, The answer is to bring a process that will run and not terminating **EX**:
```sh
docker service create --name ubuntu_serv --replicas 2 ubuntu:latest bash -c "while true; do echo hello; sleep 2; done"
```
 - **Weakness point** in Docker Swarm , it cares just the container is runing PID 1 running , if inside the container have SQL servicr and its' corrupted , Docker swarm doesn't care it just care that PID 1 is running and we have a container running.
---
## Docker Stack
 - We might consider it like docker-compose but for Swarm
 - We have new Object which is secrets and that may contain (Passowrds, keys ...)
 - bescause we have **``external: true``** in our secrets object, so we have to make sure that they exist before buildig
 - To create our secrets 
```sh
#This will Generate the certificate with its key (Key: domain.key , Cert:  domain.crt)
openssl req -newkey rsa:4096 -nodes -sha256 -keyout domain.key -x509 -days 365 -out domain.crt
```
 -  Now we have new two files **(domain.crt , domain.key)** I'll use them to create my secrets based on those files *(Use domain.key twice make 2 secrets and the domain.crt one time)*
```sh
docker secret create revprox_cert domain.crt

docker secret create revprox_key domain.key

docker secret create postgres_password domain.key

#To create a secret for staging the payment gateway:
echo staging | docker secret create staging_token - 
```
 - Check our secrets
```sh
docker secret ls
```
 - Now we're ready to build the stack
```sh
docker stack deploy -c docker-stack.yml seastack
```
 - We can check on services
```sh
docker service ls
```
*we will notice that there are created services and created networks*
> Note: in any dockerfile.yml we may use **external: true** with any object and that means that that object (Network, storadge, etc..) should have been created before building the service, and if that object wasn't there so he will create,, **BUT** if we don't use **external: true** , it will be created even it has exist and this is **overriding**
#### Weakness in docker swarm
 - Volumes are maintained on per node itself not replicated
 - No Shared image cache (if Container or node failed and i have to create on another node, it will pull the image from scratch) so it's a problem if have many images
**SO, we understand that Orchestration and service managment isn't the best in docker, it's not reliable in production**

---
## Portainer
 - It's a friendly graphical Interface for Docker (Containers, Images ,Services, Swarm,....) and help us to manage docker Environment
```sh
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml
docker stack deploy -c portainer-agent-stack.yml portainer
```
 - Go to **``https://localhost:9443/#!/home``**
![](https://i.imgur.com/pa9CTtQ.png)




