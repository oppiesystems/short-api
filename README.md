# breef

Text summarization product for distilling human verbosity.

## Development

### Development Prerequisites

```bash
virtualenv .
source bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python -c 'import nltk; nltk.download("punkt")'
```

Download models manually (Optional)

```bash
# Approximately 3gb download
mkdir models
wget -P ./models http://www.cs.toronto.edu/~rkiros/models/dictionary.txt
```

### Run

```bash
python main.py
```

### Test

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  -d @test/data.json \
  http://0.0.0.0:5900/api/shorten
```

## Deployment

### Local Docker

#### Build and run image

```bash
docker-compose up
```

#### Stop the container

Removes volumes when brought down

```bash
docker-compose down --volumes
```

### Google Cloud Platform

#### GCP Prerequisites

```bash
gcloud auth configure-docker
```

#### Build and deploy GCP image

```bash
gcloud builds submit --tag gcr.io/breef-247014/breef-image .
```

#### Run the GCP Image

```bash
docker run gcr.io/breef-247014/breef-image
```

### Additional Docker Commands

#### Tail Logs

```bash
docker logs -f breef_app
```

#### Execute Command in Container

`docker exec -t -i breef <COMMAND>`

```bash
docker exec -t -i breef_app ls models
```
