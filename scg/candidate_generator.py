import spacy
import glob
import json
import os
from multiprocessing import Pool
import multiprocessing as multi
import pickle
import scispacy
from scispacy.linking import EntityLinker
from spacy.symbols import ORTH
import time
import re
from spacy.language import Language
import pdb
import copy
from tqdm import tqdm
from scispacy.candidate_generation import CandidateGenerator

MeshCandidateGenrator = CandidateGenerator(name='mesh')
KB=MeshCandidateGenrator.kb
K=100
Resolve_abbreviations = True
Threshold = 0.3
No_definition_threshold = 0.95
Filter_for_definitions = True
Max_entities_per_mention  = 30

def candidate_dui_generator(mention_strings):
    batch_candidates = MeshCandidateGenrator(mention_strings, K)
    batched_sorted_candidates = list()
    for candidates in batch_candidates:
        predicted = []
        for cand in candidates:
            score = max(cand.similarities)
            if (
                    Filter_for_definitions
                    and KB.cui_to_entity[cand.concept_id].definition is None
                    and score < No_definition_threshold
            ):
                continue
            if score > Threshold:
                predicted.append((cand.concept_id, score))
        sorted_predicted = sorted(predicted, reverse=True, key=lambda x: x[1])
        sorted_predicted = sorted_predicted[: Max_entities_per_mention]
        batched_sorted_candidates.append(sorted_predicted)

    return batched_sorted_candidates

def batcher(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]