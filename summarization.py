#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for Text Summarization

Reference:
    - https://github.com/jatana-research/email-summarization
    - https://medium.com/jatana/unsupervised-text-summarization-using-sentence-embeddings-adb15ce83db1
"""

import numpy as np
from talon.signature.bruteforce import extract_signature
from langdetect import detect
from nltk.tokenize import sent_tokenize
from skipthoughts.skipthoughts import Encoder, load_model
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


def preprocess(strs):
    """
    Performs preprocessing operations, including:
        - Removing new line characters.
    """
    n_strs = len(strs)
    for i in range(n_strs):
        str = strs[i]
        str, _ = extract_signature(str)
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
        
        
def skipthought_encode(strs):
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
    print('Loading pre-trained models...')
    model = load_model()
    encoder = Encoder(model)
    print('Encoding sentences...')
    enc_sentences = encoder.encode(all_sentences, verbose=False)

    for i in range(len(strs)):
        begin = cum_sum_sentences[i]
        end = cum_sum_sentences[i+1]
        enc_strs[i] = enc_sentences[begin:end]
    return enc_strs
        
    
def summarize(strs):
    """
    Performs summarization of strings
    """
    n_strs = len(strs)
    summaries = [None]*n_strs

    print('Preprocessing...')
    preprocess(strs)

    print('Splitting into sentences...')
    split_sentences(strs)

    print('Starting to encode...')
    enc_strs = skipthought_encode(strs)
    print('Encoding Finished')

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
    print('Clustering Finished')

    return summaries
      