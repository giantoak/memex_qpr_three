from collections import defaultdict
from itertools import combinations
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import confusion_matrix


def get_kappas(df, columns, wt=None):
    """
    :param pandas.DataFrame df: dataframe
    :param list columns: columns with codings
    :param str wt: weight parameter for statsmodels.stats.inter_rater.cohens_kappa
    """
    from statsmodels.stats.inter_rater import cohens_kappa
    from sklearn.metrics import confusion_matrix
    from itertools import combinations
    kappa_list = []
    for col_pair in combinations(columns, 2):
        temp = df.ix[:, col_pair].dropna()
        kappa_list.append(cohens_kappa(confusion_matrix(temp[col_pair[0]], temp[col_pair[1]]), wt=wt))

    return kappa_list


def get_deltas(df, columns):
    from itertools import combinations
    delta_dict = {}
    for col_pair in combinations(columns, 2):
        temp = df.ix[:, col_pair].dropna()
        delta_dict[col_pair[0]+' '+col_pair[1]] = np.abs((temp[col_pair[0]] - temp[col_pair[1]]))

    return pd.DataFrame(delta_dict)


def main():
    """
    This doesn't really need a main() since nothing is returned.
    The function consists of a bundle of statistical metrics run on the coder data - kappa, pearson corrs, etc.
    :return:
    """
    one_case = pd.read_excel('data/coders/case/reviewer_one.xlsx', parse_cols=1)
    two_case = pd.read_excel('data/coders/case/reviewer_two.xlsx', parse_cols=1)
    three_case = pd.read_excel('data/coders/case/reviewer_three.xlsx', parse_cols=1)

    merge_cols = ['phone']
    merged_case_df = pd.merge(one_case, two_case,
                              left_on=merge_cols,
                              right_on=merge_cols,
                              suffixes=['_one', '_two'])

    merged_case_df = pd.merge(merged_case_df, three_case,
                              left_on=merge_cols, right_on=merge_cols)

    lep_fmt = 'lep_{}'.format
    lep_nrml_fmt = 'lep_{}_nrml'.format

    merged_case_df[lep_fmt('three')] = merged_case_df['law enforcement priority']
    del merged_case_df['law enforcement priority']
    for coder in ['one', 'two']:
        merged_case_df[lep_fmt(coder)] = merged_case_df['law enforcement priority_'+coder]
        del merged_case_df['law enforcement priority_'+coder]

    for coder in ['one', 'two', 'three']:
        merged_case_df[lep_nrml_fmt(coder)] = merged_case_df[lep_fmt(coder)] / (merged_case_df[lep_fmt(coder)].sum())

    case_dict = {}
    for coder_a, coder_b in combinations(['one', 'two', 'three'], 2):
        cols = merge_cols + [lep_fmt(coder_a), lep_nrml_fmt(coder_a), lep_fmt(coder_b), lep_nrml_fmt(coder_b)]
        case_dict[coder_a+'_'+coder_b] = merged_case_df.ix[:, cols].dropna()


    case_deltas = get_deltas(merged_case_df,
                             [lep_fmt(x) for x in ['one', 'two', 'three']])

    case_deltas_nrml = get_deltas(merged_case_df,
                                  [lep_nrml_fmt(x) for x in ['one', 'two', 'three']])

    for key in case_dict:
        print('Pearson Corr. for {}:'.format(key))
        a, b = key.split('_')
        print('  Standard:')
        print('    Comparison rows: {}'.format(case_dict[key].shape[0]))
        print('    Score          : {}'.format(pearsonr(case_dict[key].ix[:, lep_fmt(a)],
                                                        case_dict[key].ix[:, lep_fmt(b)])))

        temp = case_dict[key].ix[(case_dict[key][lep_fmt(a)] != 1) | (case_dict[key][lep_fmt(b)] != 1), :]
        print('  No agreed upon ones:'.format(key))
        print('    Comparison rows: {}'.format(temp.shape[0]))
        print('    Score          : {}'.format(pearsonr(temp.ix[:, lep_fmt(a)],
                                                        temp.ix[:, lep_fmt(b)])))

        temp = case_dict[key].ix[(case_dict[key][lep_fmt(a)] != 1) & (case_dict[key][lep_fmt(b)] != 1), :]
        print('  No ones at all:')
        print('    Comparison rows: {}'.format(temp.shape[0]))
        print('    Score          : {}'.format(pearsonr(temp.ix[:, lep_fmt(a)],
                                                        temp.ix[:, lep_fmt(b)])))

    one_review = pd.read_excel('data/coders/review/reviewer_one.xlsx', parse_cols=4)
    two_review = pd.read_excel('data/coders/review/reviewer_two.xlsx', parse_cols=4)
    three_review = pd.read_excel('data/coders/review/reviewer_three.xlsx', parse_cols=4)

    # Clean up
    two_review['completion'] = two_review['completion'].apply(lambda x: 'completed' if x == 'completed ' else x)
    three_review['theft'] = three_review['theft'].apply(lambda x: 'neither' if x == 'niether' else x)

    levels = dict()
    levels['completion'] = ['completed', 'not completed', 'unable to tell']
    levels['theft'] = ['theft', 'neither', 'unable to tell']
    levels['pimp'] = ['pimp', 'no pimp', 'unable to tell']

    for col in levels:
        one_review[col] = pd.Categorical(one_review[col], levels[col])
        two_review[col] = pd.Categorical(two_review[col], levels[col])
        three_review[col] = pd.Categorical(three_review[col], levels[col])

    merge_cols = ['phone', 'review id']
    merged_review_df = pd.merge(one_review, two_review,
                                left_on=merge_cols,
                                right_on=merge_cols,
                                suffixes=['_one', '_two'])

    merged_review_df = pd.merge(merged_review_df, three_review,
                                left_on=merge_cols,
                                right_on=merge_cols,
                                suffixes=['', '_three'])

    for term in ['completion', 'theft', 'pimp']:
        merged_review_df[term+'_three'] = merged_review_df[term]
        del merged_review_df[term]

    review_dict = defaultdict(dict)
    for coder_a, coder_b in combinations(['one', 'two', 'three'], 2):
        for term  in ['completion', 'theft', 'pimp']:


        cols = merge_cols + [lep_fmt(coder_a), lep_nrml_fmt(coder_a), lep_fmt(coder_b), lep_nrml_fmt(coder_b)]
        case_dict[coder_a+'_'+coder_b] = merged_case_df.ix[:, cols].dropna()


    completion_kappas = get_kappas(merged_review_df, ['completion_'+x for x in ['one', 'two', 'three']])
    theft_kappas = get_kappas(merged_review_df, ['theft_'+x for x in ['one', 'two', 'three']])
    pimp_kappas = get_kappas(merged_review_df, ['pimp_'+x for x in ['one', 'two', 'three']])
