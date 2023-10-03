import json
import os
import argparse
import hashlib

import wget
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str)
    parser.add_argument('--storage', type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    file_path = args.file_path
    storage = args.storage

    if not os.path.exists(storage):
        os.mkdir(storage)

    items = []
    unique_urls = set()
    with open(file_path, 'r') as f:
        for item in f:
            item = json.loads(item)
            if item['image_url'] not in unique_urls:
                items.append(item)
                unique_urls.add(item['image_url'])
    
    for item in tqdm(items):
        image_url = item['image_url']
        # create a unique id for each image url
        item_hash = hashlib.sha256(item['image_url'].encode()).hexdigest()
        file_path = os.path.join(storage, f'{item_hash}.png')
        wget.download(image_url, file_path)


if __name__ == '__main__':
    main()