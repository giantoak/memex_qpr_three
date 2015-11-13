import ipdb
import pandas
import json
import numpy as np
import phonenumbers
#a = pandas.read_csv('../../memexHack1/data/evidently/content_ter.tsv.gz', header=None, compression='gzip', nrows=1000, sep='\t')
nrows=None
a = pandas.read_csv('../../memexHack1/data/evidently/content_ter.tsv.gz', header=None, compression='gzip', nrows=nrows, sep='\t', names=['id','type','url','html','jsontext'], usecols=['id','type','url','jsontext'])
def get_json(x):
    try:
        me = json.loads(x)
        return(me)
    except:
        try:
            me = json.loads(x.replace('\\\\','\\'))
            return(me)
        except:
            return({})

def get_normalized_phone_review(me):
    try:
        if 'phones' in me.keys():
            if len(me['phones']):
                if len(me['phones']) > 1:
                    return( phonenumbers.format_number(phonenumbers.parse(me['phones'][0], 'US'), phonenumbers.PhoneNumberFormat.NATIONAL))
                else:
                    return( phonenumbers.format_number(phonenumbers.parse(me['phones'][0], 'US'), phonenumbers.PhoneNumberFormat.NATIONAL))
            else:
                return np.nan
        else:
            return np.nan
    except:
        return np.nan
def get_normalized_phone_text(me):
    try:
        if 'phone' in me.keys():
            if len(me['phone']):
                if len(me['phone']) > 1:
                    return( phonenumbers.format_number(phonenumbers.parse(me['phone'], 'US'), phonenumbers.PhoneNumberFormat.NATIONAL))
                else:
                    return( phonenumbers.format_number(phonenumbers.parse(me['phone'], 'US'), phonenumbers.PhoneNumberFormat.NATIONAL))
            else:
                ipdb.set_trace()
                # No elements in phone
                return np.nan
        else:
            # phones not in keys
            return np.nan
    except:
        if np.random.uniform() < .05:
            print(me['phone'])
        # Other error
        return np.nan

a['json'] = a['jsontext'].apply(get_json)
a['phone'] = a['json'].apply(get_normalized_phone_review)
np.random.seed(3)
#review_sample=np.random.choice(a[~a['phone'].isnull()].index, 300)
#sub = a.loc[review_sample]
review_sample=np.random.choice(a['phone'].unique(), 300)
sub = a[a['phone'].isin(review_sample.tolist())]
sub = sub.rename(columns={'json':'review_json'})

nrows=None
b =  pandas.read_csv('../../memexHack1/data/evidently/content_ads.tsv.gz', header=None, compression='gzip', nrows=nrows, sep='\t', names=['id','type','url','html','jsontext'], usecols=['id','type','url','jsontext'])
b['phone'] = b['jsontext'].apply(lambda x: get_normalized_phone_text(get_json(x)))

out = pandas.merge(sub, b, on='phone', how='left')
out['ad_json'] = out['jsontext_y'].apply(get_json)
out.to_csv('review_ad_sample.csv', index=False) 

print('There are %s reviews out of the sample of %s that do not match to any ads' % (out['url_y'].isnull().sum(), len(sub)))

# Create the case annotation spreadsheet
case_annotation = pandas.DataFrame({'phone':out['phone'].value_counts().index})
case_annotation['law enforcement priority'] = ''
case_annotation.to_csv('case_annotation.csv', index=False)

# Create the review annotation spreadsheet
review_annotation=pandas.DataFrame(i.groupby('phone')['id_x'].apply(lambda x: numpy.random.choice(x))).rename(columns={'id_x':'review id'}).reset_index()
review_annotation['completion'] = ''
review_annotation['theft'] = ''
review_annotation['pimp'] = ''
review_annotation.to_csv('review_annotation.csv', index=False)
