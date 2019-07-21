#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for Text Summarization

Reference:
    - https://github.com/jatana-research/email-summarization
    - https://medium.com/jatana/unsupervised-text-summarization-using-sentence-embeddings-adb15ce83db1
"""

import util, os, logging

import numpy as np
from langdetect import detect
from nltk.tokenize import sent_tokenize
from skipthoughts.skipthoughts import Encoder, load_model, path_to_tables, path_to_umodel, path_to_bmodel
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

MODEL_BUCKET = os.environ.get('MODEL_BUCKET', 'breef-models')
logger = logging.getLogger()

def preprocess(strs):
    """
    Performs preprocessing operations, including:
        - Removing new line characters.
    """
    n_strs = len(strs)
    for i in range(n_strs):
        str = strs[i]
        lines = str.split('\n')
        for j in reversed(range(len(lines))):
            lines[j] = lines[j].strip()
            if lines[j] == '':
                lines.pop(j)
        strs[i] = ' '.join(lines)

        
def split_sentences(strs):
    """
    Splits the strings into individual sentences
    """
    n_strs = len(strs)
    for i in range(n_strs):
        str = strs[i]
        sentences = sent_tokenize(str)
        for j in reversed(range(len(sentences))):
            sent = sentences[j]
            sentences[j] = sent.strip()
            if sent == '':
                sentences.pop(j)
        strs[i] = sentences
        
        
def skipthought_encode(strs, model):
    """
    Obtains sentence embeddings for each sentence in the strings
    """
    enc_strs = [None]*len(strs)
    cum_sum_sentences = [0]
    sent_count = 0
    for str in strs:
        sent_count += len(str)
        cum_sum_sentences.append(sent_count)

    all_sentences = [sent for str in strs for sent in str]
    encoder = Encoder(model)
    logger.info('Encoding sentences...')
    enc_sentences = encoder.encode(all_sentences, verbose=False)

    for i in range(len(strs)):
        begin = cum_sum_sentences[i]
        end = cum_sum_sentences[i+1]
        enc_strs[i] = enc_sentences[begin:end]
    return enc_strs
        
    
def summarize(strs, model=None):
    """
    Performs summarization of strings
    """
    if model == None:
        model = load_models()

    n_strs = len(strs)
    summaries = [None]*n_strs

    logger.info('Preprocessing...')
    preprocess(strs)

    logger.info('Splitting into sentences...')
    split_sentences(strs)

    logger.info('Starting to encode...')
    enc_strs = skipthought_encode(strs, model)
    logger.info('Encoding Finished')

    for i in range(n_strs):
        enc_str = enc_strs[i]
        n_clusters = int(np.ceil(len(enc_str)**0.5))
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans = kmeans.fit(enc_str)
        avg = []
        closest = []

        for j in range(n_clusters):
            idx = np.where(kmeans.labels_ == j)[0]
            avg.append(np.mean(idx))

        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,\
                                                enc_str)
        ordering = sorted(range(n_clusters), key=lambda k: avg[k])
        summaries[i] = ' '.join([strs[i][closest[idx]] for idx in ordering])
    logger.info('Clustering Finished')

    return summaries


def download_models(gs_bucket, _logger=logger):
    """ 
    Downloads missing models dependencies, locally, if they don't exist already. 
    """
    dependencies = [
        path_to_umodel,
        '%s.pkl' % path_to_umodel,
        path_to_bmodel,
        '%s.pkl' % path_to_bmodel,
        '%sutable.npy' % path_to_tables,
        '%sbtable.npy' % path_to_tables,
        '%sdictionary.txt' % path_to_tables
    ]

    for _, filePath in enumerate(dependencies):
        # Creates directory if it doesn't exist
        directory = os.path.dirname(filePath)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Downloads dependency from Google Cloud Storage
        if (os.path.isfile(filePath) != True):
            try:
                _logger.info('Downloading: \'%s\'...' % filePath)
                util.download_blob(gs_bucket, filePath, filePath)
            except Exception as e:
                _logger.error(e)

def load_models(_logger=logger):
    download_models(MODEL_BUCKET, _logger)

    _logger.info('Loading pre-trained models...')
    return load_model()