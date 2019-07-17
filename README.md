# breef

Text summarization product for distilling human verbosity.

## Setup

```bash
virtualenv .
source bin/activate
```

### Install

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

## Run

```bash
python main.py
```
