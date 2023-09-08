import pandas as pd

from crawler.vcsheet.vcsheet_contact_crawler import VcsheetCrawler


def prune_result(df):
    def label_bad(email):
        return not isinstance(email, str) or email.endswith('.webpack') or email.endswith('.png') or email.endswith('.jpeg') or email.endswith('.jpg') or email.endswith('.wixpress.com') or email.endswith('.sentry.io') or 'firstnamelastname' in email
    
    # post evaluation
    df = pd.read_csv('./emails.csv')
    df = df[df['emails'] != 'angelgarcia.mail@gmail.com']
    df['is_bad'] = df['emails'].apply(label_bad)
    df = df[~df['is_bad']]
    df['emails'] = df['emails'].apply(lambda email: email.lstrip('u003e'))

    del df['is_bad']
    return df


if __name__ == '__main__':
    crawler = VcsheetCrawler(
        crawler_directory='./result_vcsheet',
    )

    df = crawler.run()
    df = prune_result(df)
    df.to_csv('./result_vcsheet/data/pruned_investor_contacts.csv', index=False)