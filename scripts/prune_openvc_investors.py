import sys
import pandas as pd


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


def main():
    file_path = sys.argv[0]
    df = pd.read_csv(file_path)
    df = prune_result(df)
    df.to_csv(file_path.replace('.csv', '') + '_pruned.csv', index=False)


if __name__ == '__main__':
    main()
    