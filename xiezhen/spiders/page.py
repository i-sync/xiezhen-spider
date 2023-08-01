import time
import scrapy

from scrapy.exceptions import DropItem
from xiezhen.models import session_scope, Posts, Tags
from xiezhen.items import CategoryItem, PageItem


class PageSpider(scrapy.Spider):
    name = 'page'
    allowed_domains = ['www.xiezhen.xyz']
    start_urls = ['https://www.xiezhen.xyz/page']

    custom_settings = {
        'ITEM_PIPELINES': {
            'xiezhen.pipelines.CategoryPipeline': 200,
            'xiezhen.pipelines.PagePipeline': 300
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=f"{url}/1", callback=self.parse, meta={"page_number": 1})

    def parse(self, response):

        links = response.xpath("//div[@class='excerpts']/article/a/@href").extract()
        for l in links:
            yield scrapy.Request(url = l, callback=self.detail_parse)
            # break


        total = response.xpath("//div[@class='pagination pagination-multi']/ul/li[last()-1]/a/@href").extract_first().strip().split('/')[-1]
        if total.isdigit():
            total = int(total)

        page_number = response.meta["page_number"] if "page_number" in response.meta else 1
        page_number += 1
        #if page_number <= last_page:
        if page_number <= 10: # total:
            next_url = f"{self.start_urls[0]}/{page_number}"
            print(page_number, "next page", next_url)
            yield scrapy.Request(url = next_url, callback=self.parse, meta={"page_number": page_number})

    def detail_parse(self, response):
        category_name = response.css("div.article-meta span.item-3 a").xpath("@href").extract_first().strip().split('/')[-1]
        category = None
        with session_scope() as session:
            category = session.query(Tags).filter(Tags.name == category_name).first()

        if not category:
            category = CategoryItem()
            category_title = response.css("div.article-meta span.item-3 a::text").get()
            category["title"] = category_title
            category["name"] = category_name
            yield category

            # wait 1s
            time.sleep(1)
            yield response.follow(url = response.request.url, callback = self.detail_parse, dont_filter=True)
        else:


            title = response.xpath("//header[@class='article-header']/h1[@class='article-title']/text()").extract_first().strip()
            date = response.xpath("//header[@class='article-header']/div[@class='article-meta']/span[@class='item item-1']/text()").extract_first().strip().replace('下午', 'PM').replace('上午','AM')
            date = time.strptime(date, '%Y年%m月%d日 %p%H:%M')

            images = response.xpath("//article[@class='article-content']/p/img/@src").extract()
            video_url = response.xpath("//article[@class='article-content']/div[@class='wp-video']/video/source/@src").extract_first()


            item = PageItem()
            item["post_type"] = "image"
            if not len(images) and video_url:
                item["post_type"] = "video"
            item["post_title"]= title
            item["origin_created_at"]= time.strftime('%Y-%m-%d %H:%M:%S', date)
            item["origin_link"]= response.request.url
            item["post_media"]= images[0] if len(images) else None
            item["post_slug"]= response.request.url.split('/')[-1]
            item["media_alt"]= title
            item["images"]= images
            item["post_video"] = video_url
            item["video_url"] = video_url

            item["category_id"]= category.id
            yield item