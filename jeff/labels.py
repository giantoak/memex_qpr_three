import pandas
a = pandas.read_csv('reviews_url_phone_flags.tsv', sep='\t', header=None, names=['url','phones','labels'])
a[a['labels'].isnull()]=''
b=a['labels'].value_counts().index.tolist()
b=[i for i in b if ',' not in i and i is not '']
for i in b:
    a[i] = a['labels'].apply(lambda x: i in x)

a=a[b]
print('unconditional correlations in the data:')
print(pandas.DataFrame.corr(a))
pandas.DataFrame.corr(a).to_csv('label_correlations.csv')

print('correlations conditional on having at least 1 label extracted')
print(pandas.DataFrame.corr(a[a.sum(axis=1)>0]))
pandas.DataFrame.corr(a[a.sum(axis=1)>0]).to_csv('label_correlations_postitve.csv')
a=a[a.sum(axis=1)>0] 


#Organized
print('correlations conditional on being "organized"')
print(pandas.DataFrame.corr(a[a['Organized']]))
pandas.DataFrame.corr(a[a['Organized']]).to_csv('label_correlations_organized.csv')
