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

Download models

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
