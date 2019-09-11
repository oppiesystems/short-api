# breef

Text summarization product for distilling human verbosity.

## Development

### Development Prerequisites

```bash
npm run preinstall
```

*OR*

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

#### Unit Test

Execute the following command to run the unit test package for the project.

```bash
npm test

--or--

python -m unittest -v test # Verbose
```

#### API

`POST /digest`

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  -d @test/post_data.json \
  http://0.0.0.0:5900/api/digest
```

## Deployment

### Local Docker

#### Build image

```bash
docker build -t breef:latest .
```

#### Run image

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
gcloud builds submit --config cloudbuild.yaml .
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
