# Webscraping Buddy

A minimum set of development toolkits for developing web crawlers.


## Setup
```bash
poetry install
```

## How to use?
### Create a crawler
You can create a new crawler by subclassing from the BaseCrawler. The run() method of your crawler contains the crawling logic.
```python

class VcsheetCrawler(BaseCrawler):
    def run(self):
        investor_file_path = os.path.join(self.store_directories['cache'], INVESTORS_FILE_NAME)
        if not os.path.exists(investor_file_path):
            investors_page = InvestorsPage()
            df_investors = investors_page.get_investors()
            self.write_df('cache', df_investors, INVESTORS_FILE_NAME)
        else:
            df_investors = pd.read_csv(investor_file_path)

        ...
```
### Run the Crawler
The Crawler takes 1 argument `crawler_directory`, which is the directory of storing cache results (`<crawler_directory>/cache`) and the final results (`<crawler_directory>/data`). You can find the results of the crawler in `<crawler_directory>/data`.
```python
from crawler.openvc.openvc_contact_crawler import OpenvcContactCrawler


crawler = OpenvcContactCrawler(
    crawler_directory='./result_openvc',
)

df = crawler.run()
```

## Cases
### 1. Collect a list of contacts of investors and VCs



## Doc
```python

```