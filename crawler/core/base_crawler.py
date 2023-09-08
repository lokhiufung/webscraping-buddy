import os


class BaseCrawler:
    def __init__(self, crawler_directory):
        self.crawler_directory = crawler_directory
        self.data_directory = os.path.join(self.crawler_directory, 'data')
        self.cache_directory = os.path.join(self.crawler_directory, 'cache')

        if not os.path.exists(self.crawler_directory):
            os.mkdir(self.crawler_directory)
            os.mkdir(self.data_directory)
            os.mkdir(self.cache_directory)

        self.store_directories = {
            'data': self.data_directory,
            'cache': self.cache_directory,
        }

    def write_df(self, store_type, df, file_name, **kwargs):
        df.to_csv(os.path.join(self.store_directories[store_type], file_name), index=False, **kwargs)

    def write_html(self, store_type, html_content, file_name):
        file_path = os.path.join(self.store_directories[store_type], file_name)
        with open(file_path, 'w') as f:
            f.write(html_content)
    


