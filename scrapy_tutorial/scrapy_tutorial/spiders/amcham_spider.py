import scrapy


class AmchamBusinessSpider(scrapy.Spider):
    name = 'amchamBusinessSpider'
    start_urls = [
        'https://topics.amcham.com.tw/category/industry-focus/',
        'https://topics.amcham.com.tw/category/taiwan-business/'
    ]

    # Custom settings to address potential blocks
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False,  # Disable obeying robots.txt
        'COOKIES_ENABLED': True,  # Enable cookies to maintain session
        'RETRY_ENABLED': True,    # Enable retries for failed requests
        'RETRY_TIMES': 5,         # Retry up to 5 times
        'DOWNLOAD_DELAY': 1.0,    # Add delay between requests to avoid being blocked
    }

    def smart_truncate(self, content, length=163, suffix='...'):
        """
        Truncate content to a specified length, preserving whole words and adding a suffix.
        """
        if len(content) <= length:
            return content
        else:
            return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix

    def parse(self, response):
        """
        Parse the response to extract the required data from the articles.
        """
        if response.status == 403:
            self.logger.warning(f"Access denied for URL: {response.url}")
            return

        for post in response.css('article'):
            try:
                yield {
                    'Topic': post.css('.entry-title a::text').get(default='N/A'),
                    'Blurb': self.smart_truncate(post.css('.entry-summary p::text').get(default='')),
                    'Image': post.css('img::attr(src)').get(default=''),
                    'Link': post.css('.entry-title a::attr(href)').get(default=''),
                    'OP': "Taiwan Business Topics"
                }
            except Exception as e:
                self.logger.error(f"Error processing post: {e}")

    def handle_spider_closed(self):
        self.logger.info("Spider closed. Ensure all data is saved correctly.")
