import pandas as pd


def main():
    """
    This function is predicated on having a slice of ads and phone numbers called 'review_ad_sample.csv.gz' in the same directory as this file.
    """
    hyperlink_fmt = '=HYPERLINK("http://memex.deepdivedata.org:8001/#/search/?t=everything&n=10&p=1&s=phones: %22{phone}%22", "{phone}")'.format

    df = pd.read_csv('review_ad_sample.csv.gz')
    df['Evidently LE'] = df['phone'].apply(lambda x: hyperlink_fmt(phone=x))

    # Get phone subset
    phone_df = df.ix[:, ['phone', 'Evidently LE']]
    phone_df.drop_duplicates(inplace=True)
    phone_df.reset_index(inplace=True)
    phone_df['Priority?'] = ''
    phone_df['John quit?'] = ''
    phone_df['Robbery or theft by provider?'] = ''
    phone_df['Reference to pimp?'] = ''

    # Dump to a number of excel files
    excel_fmt = 'Evidently LE Phones, Bundle {bnum}, Copy {cnum}.xlsx'.format

    rows_per_file = 25
    copy_count = 2

    bnum = 1
    for i in range(0, phone_df.shape[0], rows_per_file):
        for cnum in range(1, copy_count+1):
            phone_df.ix[i:(i+rows_per_file), ['Evidently LE', 'Priority?', 'John quit?', 'Robbery or theft by provider?', 'Reference to pimp?']].to_excel(excel_fmt(bnum=bnum, cnum=cnum), index=False)
        bnum += 1


if __name__ == "__main__":
    main()
