import json
import sys

import pandas as pd


def prune_result(df):
    def label_bad(email):
        return not isinstance(email, str) or email.endswith('.webpack') or email.endswith('.png') or email.endswith('.jpeg') or email.endswith('.jpg') or email.endswith('.wixpress.com') or email.endswith('.sentry.io') or 'firstnamelastname' in email
    
    # post evaluation
    df = df[df['email'] != 'angelgarcia.mail@gmail.com']
    df['is_bad'] = df['email'].apply(label_bad)
    df = df[~df['is_bad']]
    df['email'] = df['email'].apply(lambda email: email.lstrip('u003e'))

    del df['is_bad']
    return df


def main():
    file_path = sys.argv[1]
    df = []
    # assumed jsonl
    with open(file_path, 'r') as f:
        for record in f:
            df.append(json.loads(record))
    df = pd.DataFrame(df)
    df = prune_result(df)
    df.to_csv(file_path.replace('.jsonl', '') + '_pruned.csv', index=False)


if __name__ == '__main__':
    main()
    