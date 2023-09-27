# Webscraping Buddy

This repository serve as a practice of web scraping. The web srapers may be useful for influencer marketing and lead generation. However please be careful when you are using the scraper and be nice to the websites.

## Setup
```bash
poetry install
```

## Use cases
### Use case 1: Lead Generation in Fund-raising
The crawlers will gather initaial data (investor'name, linkedin, investor's website) from investor listing websites. Then, the scraper will extract directly the email directly from many investor / venture capital official websites.

An contact record may look like the following:
```json
{
    "investor_name": "Bullish",
    "email": "hey@bullish.co",
    "linkedin": "https://www.linkedin.com/company/bullish-inc",
    "website": "http://bullish.co/",
    ...
}

```

Now there are scrapers for [openvc.app](https://openvc.app) and [vcsheet](https://vcsheet/investors). Please note that now they may only be able to generate like 100 of the contact records and you should also need to vallidate those email extracted because they are automatically extracted from the investor / venture capital websites.

You can start the crawlers with the following:
#### OpenVC
1. Navigate to the scrapy_crawler directory first.
```bash
cd scrapy_crawler
```
2. Start the `openvc_investors` crawler
```bash
scrapy crawl openvc_investors
```

#### VCSheet
1. Run the interactive crawler
```bash
# assumed .jsonl as the output format
python run_interactive_crawler.py --project investors --spider vcsheet_investors --storage vcsheet_investors.jsonl
```

### Use case 2: Influencer Discovery
Influencer marketing is one of the popular options for efficient marketing today. You need a list of potential influencer with high ROI before you start a influencer marketing campaign. The potential high-quailty influencers can be found in the trend posts in social media, like Instagram, Xiao Hung Shu (i.e a popular instagram-like social media app in China). There are crawlers to gather the accounts with high number of followers in the trendin posts in the social media.

For example, an account record may look like the following:
```json
{
    "url": "https://www.xiaohongshu.com/user/profile/61371cd1000000000202278b",
    "image_url": "https://sns-avatar-qc.xhscdn.com/avatar/616453e18ff10217afbb347f.jpg?imageView2/2/w/540/format/webp|imageMogr2/strip2", "user_name": "\u590f\u51c9\u51c9",
    "user_id": "\u5c0f\u7ea2\u4e66\u53f7\uff1a4993455596",
    "user_ip": "IP\u5c5e\u5730\uff1a\u4e0a\u6d77",
    "user_desc": "\ud83d\udce995413366@qq.com\n\ud83c\udf90\u624b\u5199 | \u60c5\u611f | \u597d\u7269\u5206\u4eab\n\ud83d\udeab\u7981\u6b62\u642c\u8fd0\uff0c\u53d1\u73b0\u76f4\u63a5\u4e3e\u62a5",
    "user_interactions": [{"\u5173\u6ce8": "10+"}, {"\u7c89\u4e1d": "10W+"}, {"\u83b7\u8d5e\u4e0e\u6536\u85cf": "200W+"}],
    "_tsCrawled": 1694923402
}
```
#### Xiao Hung Shu
1. Run the interactive crawler
```bash
# assumed .jsonl as the output format
python run_interactive_crawler.py --project xhs --spider influencers --storage xhs_influencers.jsonl
```

### Use case 3: Extracting images from public accounts
Instagram is a great place to get a large amount of high quailty images for research (e.g cats). This is useful when you want to study image generation / recognition models

```bash
python run_interactive_crawler.py --project ig --spider public_images --storage public_images.jsonl --config_file public_images_spider_config.json 
```

```json
{
    "image_url": "https://instagram.fyto1-1.fna...",
    "account": "<account name>",
    "_tsCrawled": 1695827875
}
```

## Pruning the crawled data
You have to prune the crawled data. We are mining emails over 1000 of websites. There is no guarantee that you can extract the emails from the company webistes. You can use the following scripts to prune your results

### VC Sheet
```bash
python scripts/prune_vcsheet_investors.py ./crawled_data/vcsheet/investors.jsonl
```

### OpenVC
```bash
python scripts/prune_openvc_investors.py ./crawled_data/openvc/investors.jsonl
```

## scrapy_crawler
This folder contains the crawlers built with Scrapy. Scrapy is an excellent tool for building crawlers. It can provide stability, concurrent, bug-free and exceptional error handling for web scraping to users.

## interactive_crawler
If scrapy is so good, why there is another crawler here? The answer is that I find when integrating scrapy with playwright, it is super hard to debug. I have spent a half day to investigate why the vcsheet_investors_spider.py is not working but still have no clue (anyone can help will be great!). Then I decide to use half an hour to write the crawler purely with playwright. That's why you can see there are 2 vcsheet crawlers in both interactive_crawler and scrapy_crawler.

### Doc
### Interactive Spider
TODO
