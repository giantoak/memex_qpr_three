import codecs
import numpy as np
import os
import pandas as pd


def initialize_cdr_es():
    from elasticsearch import Elasticsearch
    return Elasticsearch(['https://memex:3vYAZ8bSztbxmznvhD4C@els.istresearch.com:19200/memex-domains/'],
                         verify_certs=False)


def get_cdr_exact_key_filter_dsl(key, value_or_values):
    """
    Take a key and value (or list of values) and return a dict for use with Query DSL that will match it exactly.
    :param str key: The key
    :param value_or_values: A value or list of values
    :return dict: A dictionary compatible with Elasticsearch's Query DSL
    """
    return {"query": {"filtered": {"filter": {"term": {key: value_or_values}}}}}


def main():
    cpcs = pd.read_excel('data/challenge_problem_one/original/Challenge Problem Clusters.xlsx', sheetname=None)
    all_ad_ids = np.concatenate([cpcs[cpc_key].iloc[:, 1].values for cpc_key in cpcs], axis=0)

    df = pd.read_table('data/challenge_problem_one/original/url_phone_flags.tsv',
                       index_col=False, names= ['url', 'phone', 'flags'])

    df.ix[:, 'flags'] = df.ix[:, 'flags'].fillna('').apply(lambda x: x.split(','))
    all_flags = set(np.concatenate(df['flags'].values, axis=0))
    all_flags.remove('')
    for flag in all_flags:
        df[flag] = df['flags'].apply(lambda x: flag in x)
    del df['flags']

    df.ix[:, 'phone'] = df.ix[:, 'phone'].fillna('').apply(lambda x: x.replace('(', '').replace(')', '').
                                                           replace('-', '').replace(' ', '').split(','))

    if not os.path.exists('data/challenge_problem_one/generated'):
        os.mkdir('data/challenge_problem_one/generated')
    df.to_pickle('data/challenge_problem_one/review_phones_and_codes.pkl')

    all_phones = set(np.concatenate(df['phone'].values, axis=0))
    all_phones.remove('')


if __name__ == "__main__":
    main()
