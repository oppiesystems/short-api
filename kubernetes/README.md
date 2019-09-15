# Google Cloud Platform + Kubernetes Instantiation

- Create project in Google Cloud Console.

- Set environment credentials

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/pat/Keys/oppie/breef-admin.json
```

--or--

```bash
gcloud auth application-default login
```

- Create new `gcloud` configuration.

```bash
gcloud config configurations create breef
```

- Instantiate new `gcloud` configuration.

```bash
gcloud init
```

- Enter `1` for "Re-initialize this configuration [high-pops-dev] with new settings"

- Select main acocunt.

- Pick the newly created project.

- Configure default zone.

- Verify current project is set.

```bash
gcloud config list
```

- Create Kubernetes Container Cluster by running the following:

```bash
gcloud container clusters create breef-cluster
```

- Set default to cluster.

```bash
gcloud config set container/cluster high-pops-dev-cluster
```

- Within Google Cloud Console, navigate to the newly created cluster and select "Connect" to get the following:

```bash
gcloud container clusters get-credentials breef-cluster --zone us-west1-b --project breef-247014
```

- __Optional__: Start a proxy to the cluster by running the follow

```bash
kubectl proxy
```

- Build the Google Cloud image.

__Note__: Uses `root` priveleges to copy files from mounted `models` volume.

```bash
sudo docker build -t gcr.io/breef-247014/breef_api -f ./docker/api/Dockerfile .
```

- Push image to the container registry.

```bash
gcloud docker -- push gcr.io/breef-247014/breef_api
```

- Changes to `kubernetes` directory.

```bash
cd kubernetes
```

- __Optional__: Create Kubernetes a deployment file from `docker-compose.yml` using `kompose`.

```bash
kompose convert -o deployment.yml
```

- Start Kubernetes cluster.

```bash
kompose up
```

--or--

```bash
kubectl create -f deployment.yml
```

- __Optional__: Expose application locally.

```bash
kubectl port-forward service/api 5900:5900
```

## Expose Application Publicly

- __Optional__: Create static IP address.

```bash
gcloud compute addresses create short-dev-ip --global
```

- Create an Ingress service.

```bash
kubectl create -f ingress-service.yml
```

- Verify exposed IP

```bash
kubectl get ingress
```

### SSL

Add SSL certificates downloaded from Cloudflare.

```bash
gcloud compute ssl-certificates create ingress  \
  --certificate /home/pat/Keys/oppie/certs/oppie.io.pem \
  --private-key /home/pat/Keys/oppie/certs/oppie.io.key

kubectl apply -f ingress-service.yml
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
