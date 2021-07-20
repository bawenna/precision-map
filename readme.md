# Precision Map

<br>

### About
This is a simple widget to process the log files in order to automate the quality control evaluation and display the result.

### Local Development Setup
1) Install Python3, then run pip3 install -r requirements.txt to install flask and waitress
2) Run waitress-serve --listen=*:5000 app:app to access the application via localhost:5000

### Local Kubenetes Setup
1) Install Kind: [Link](https://kind.sigs.k8s.io/docs/user/quick-start/)
2) Under the k8s directory, run kind create cluster --config kind-ingress-local.yaml --image kindest/node:v1.18.8 to start off a local cluster
3) Run kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml to deploy a Nginx Ingress Controller
4) Under the k8s directory, run kubectl apply -f manifest-local.yml to start off our application
5) Visit localhost to see the hosted application

### kubectl & eksctl
1) Install Kubectl
2) Install Lens (Optional)
2) Install eksctl
3) Make IAM profile
**Note: Minimum IAM Policy are required for eksctl. Please refer the doc** [Link](https://eksctl.io/usage/minimum-iam-policies/)
4) Install aws-cli and run aws configure, use the AWS_ACCESS_KEY_ID and AWS_ACCESS_KEY_SECRETS from the account you created 
5) Run the following command: eksctl create cluster --name precision-map --version 1.20 --region us-east-2 --nodegroup-name linux-nodes --node-type t2.micro --nodes 2
6) This will create a eks cluster with appropriate VPC/SG/Subnet/ELB to deploy
7) Run aws eks update-kubeconfig --name precision-map --region us-east-2 to merge the kube config to local machine
8) Under the k8s folder, run kubectl apply -f manifest.yml to deploy the application to the cluster
9) You can access to application by visiting the elb DNS name.

### Terraform
Followed guide here for initializing the cluster: [Link](https://learn.hashicorp.com/tutorials/terraform/eks)
1) You need to configure an IAM user with appropriate permission to create the EKS cluster: [Link](https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/docs/iam-permissions.md)
2) Run terraform init to initialize the enviornment
3) Run terraform plan to examine the output
4) Run terraform apply to deploy the eks cluster with the hosted application

### Docker
1) Install Docker on local machine [Link](https://docs.docker.com/engine/install/)
2) Make Docker Hub Account. [Link](https://hub.docker.com)
3) Add Docker repository. Note: Keep the repository public for Kubernetes cluster to access it freely.
4) Build Docker Image on local machine.
```shell
docker build -t <your docker repo>:<tag> .
```
5) Push the image to docker hub.
```shell
docker push <your docker repo>:<tag>
``` 

