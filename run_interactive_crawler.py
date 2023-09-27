import json
import time
import argparse
from importlib import import_module

from interactive_crawler.jsonl_pipeline import JsonlPipeline
from interactive_crawler.logger import get_logger


logger = get_logger('interactive_crawler', logger_lv='debug')


def snake_to_camel(name):
    return ''.join(word.capitalize() for word in name.split('_'))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=str, help='name of the project')
    parser.add_argument('--spider', type=str, help='name of the spider')
    parser.add_argument('--storage', type=str, help='file path of the output folder')
    parser.add_argument('--batch_size', type=str, default=5, help='batch size of the pipeline')
    parser.add_argument('--headless', action='store_true', help='use headless mode')
    parser.add_argument('--random_user_agent', action='store_true', help='use random user agent')
    parser.add_argument('--config_file', type=str, help="additional parameters for spider")
    return parser.parse_args()


def main():
    args = parse_args()
    project_name = args.project + '_spiders'
    spider_name = args.spider + '_spider'
    file_path = args.storage
    batch_size = args.batch_size
    # spider arguments
    headless = args.headless
    random_user_agent = args.random_user_agent
    # config
    config_file = args.config_file

    item_buffer = []
    # project_name = 'xhs_spiders'
    # spider_name = 'trending_posts_spider'
    # file_path = './testing.jsonl'
    
    # start the item pipeline
    item_pipeline = JsonlPipeline(file_path)
    # load spider config
    with open(config_file, 'r') as f:
        spider_config = json.load(f)
    # import the spider
    spider_module = import_module(f'interactive_crawler.spiders.{project_name}.{spider_name}')
    spider = getattr(spider_module, snake_to_camel(spider_name))(
        # temp
        headless=headless,
        options=None,
        user_agent=None,
        randomize_user_agent=random_user_agent,
        config=spider_config,
    )
    # start the spider
    spider.start()
    item_counts = 0
    iteration_counts = 0
    done = False
    item_iterator = spider.parse()
    try:
        while not done:
            iteration_counts += 1
            try:
                item = next(item_iterator)
                item['_tsCrawled'] = int(time.time())
                # count how many items have beed extracted
                item_counts += 1
                item_buffer.append(item)
            except StopIteration:
                logger.info('Finished crawling items')
                done = True
            except Exception as err:
                logger.error(err)
            # # write item
            # item_pipeline.write(item)
            if len(item_buffer) >= batch_size:
                item_pipeline.batch_write(item_buffer)
                # reset the item_buffer after batch write
                item_buffer = []
            if iteration_counts > 0 and iteration_counts % 20 == 0:
                logger.info(f'{item_counts} items were extracted in {iteration_counts} iterations.')
    finally:
        # stop the spider
        logger.info('Stop the spider gracefully.')
        # clear the item_buffer
        if item_buffer:
            item_pipeline.batch_write(item_buffer)
        spider.stop()


if __name__ == '__main__':
    main()