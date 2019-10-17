# Google Cloud Platform

## Project Instantiation

Create project in Google Cloud Console.

Set environment credentials

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/pat/Keys/oppie/breef-admin.json
```

--or--

```bash
gcloud auth application-default login
```

Create new `gcloud` configuration.

```bash
gcloud config configurations create breef
```

Instantiate new `gcloud` configuration.

```bash
gcloud init
```

- Enter `1` for "Re-initialize this configuration [breef-project] with new settings"

- Select main acocunt.

- Pick the newly created project.

- Configure default zone.

Verify current project is set.

```bash
gcloud config list
```

## Kubernetes Cluster Instantiation

Create Kubernetes Container Cluster by running the following:

```bash
gcloud container clusters create short-dev-cluster
```

Set default to cluster.

```bash
gcloud config set container/cluster short-dev-cluster
```

Within Google Cloud Console, navigate to the newly created cluster and select "Connect" to get the following:

```bash
gcloud container clusters get-credentials breef-cluster --zone us-west1-b --project breef-247014
```

### Optional: Start a proxy to the cluster by running the follow

```bash
kubectl proxy
```

## Build

Build the Google Cloud image.

__Note__: Uses `root` priveleges to copy files from mounted `models` volume.

```bash
sudo docker build -t gcr.io/breef-247014/breef_api -f ./docker/api/Dockerfile .
```

Push image to the container registry.

```bash
gcloud docker -- push gcr.io/breef-247014/breef_api
```

## Deployment

Change to `kubernetes` directory.

```bash
cd kubernetes
```

### Prerequisite: Instantiate Storage

Deploy the PersistentVolumeClaim `pvc.yml` for storing the model files

```bash
kubectl create -f pvc.yml
```

### __Optional__: Generate Deployment Configuration

Create a Kubernetes deployment file from `docker-compose.yml` using `kompose`

```bash
kompose convert -o deployment.yml
```

### Deploy to Kubernetes

Start Kubernetes cluster.

```bash
kubectl create -f deployment.yml
```

### Prerequisite: Transfer File Dependencies

Copy model files from Google Cloud Store to mounted volume

```bash
curl https://sdk.cloud.google.com | bash
```

```bash
exec -l $SHELL
```

```bash
gcloud init
```

```bash
breef-247014
```

```bash
mkdir -p /mnt/disk/models
gsutil rsync gs://$GCS_BUCKET /mnt/disk/models
```

## Expose Application Publicly

__Optional__: Create static IP address.

```bash
gcloud compute addresses create short-dev-ip --global
```

Create an Ingress service.

```bash
kubectl create -f ingress-service.yml
```

Verify exposed IP

```bash
kubectl get ingress
```

### SSL/TLS

Add SSL certificates downloaded from Cloudflare.

```bash
gcloud compute ssl-certificates create ingress  \
  --certificate /home/pat/Keys/oppie/certs/oppie.io.pem \
  --private-key /home/pat/Keys/oppie/certs/oppie.io.key

kubectl apply -f ingress-service.yml
```

## Resource Pools

### Upgrade Resources

Use the [console](https://console.cloud.google.com/kubernetes/clusters/) or via the command-line interface:

Create a pool with a specified `machine-type` and cluster size.

```bash
gcloud container node-pools create medium-pool \
  --cluster=short-dev \
  --machine-type=n1-highmem-2 \
  --num-nodes 1 --enable-autoscaling
  --min-nodes 1 --max-nodes 3
```

#### Cordon

Cordon (or unschedule) nodes in existing pool, where `larger-pool` is the name of the node pool.

```bash
for node in $(kubectl get nodes -l cloud.google.com/gke-nodepool=larger-pool -o=name); do
  kubectl cordon "$node";
done
```

#### Evict

Drain (or evict) nodes in existing pool, where `larger-pool` is the name of the node pool.

```bash
for node in $(kubectl get nodes -l cloud.google.com/gke-nodepool=larger-pool -o=name); do
  kubectl drain --force --ignore-daemonsets --delete-local-data --grace-period=10 "$node";
done
```

__Note__: A GPU can be used with a `nvidia-tesla-t4` machine type.

### Examine Pool

```bash
gcloud container node-pools describe larger-pool \
    --cluster short-dev
```

### Delete Pool

__Note__: Cordon and evict node resources prior to deleteing pool.

```bash
gcloud container node-pools delete larger-pool \
    --cluster short-dev
```

## Debug

View status of Kubernetes

```bash
kubectl get deployment,svc,pods,pvc,ingress
```

Details about pod (e.g. looking for crashes)

```bash
kubectl describe pod/<POD_NAME>
```

Execute a command within a pod

```bash
kubectl exec -it <POD_NAME> -- /bin/bash
```

### Optional: Expose application locally

```bash
kubectl port-forward service/api 5900:5900
```
