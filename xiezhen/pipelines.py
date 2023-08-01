# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from datetime import datetime

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from xiezhen.items import PageItem, CategoryItem
from xiezhen.models import session_scope, Posts, Tags, Post_Tag, Contents

class XiezhenPipeline:
    def process_item(self, item, spider):
        return item

class PagePipeline:

    def process_item(self, item, spider):

        if isinstance(item, CategoryItem):
            return item

        post_slug = item["post_slug"]
        with session_scope() as session:
            post = session.query(Posts).filter(Posts.post_slug == post_slug).first()
        if post:
            return DropItem(f"Post exists, {post.post_title}, {post.post_slug}")

        model = Posts()
        model.user_id = 1 # admin
        model.post_live = 1
        model.post_color = 'bg-primary'
        model.post_title = item["post_title"]
        model.post_desc = item["post_title"]
        model.post_media = item["post_media"]

        model.post_slug = item["post_slug"]
        model.media_alt = item["media_alt"]
        model.origin_link = item["origin_link"]
        model.origin_created_at = item["origin_created_at"]

        model.counter = 0

        model.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        category_id = item["category_id"]
        images = item["images"]
        model.post_video = item["post_video"]
        model.video_url = item["video_url"]

        with session_scope() as session:
            session.add(model)
            session.flush()
            post_id = model.id

            post_tag = Post_Tag()
            post_tag.post_id = post_id
            post_tag.tag_id = category_id
            session.add(post_tag)

            if images and item["post_type"] == "image":
                for img in images:
                    image = Contents()
                    image.post_id = post_id
                    image._type = "image"
                    image.body = img
                    session.add(image)

            # commit
            session.commit()
        print(f"post commit, title: {item['post_title']}")

class CategoryPipeline:

    def process_item(self, item, spider):

        if isinstance(item, PageItem):
            return item

        with session_scope() as session:
            category = session.query(Tags).filter(Tags.name == item["name"]).first()
        if category:
            return DropItem(f"category exists, {category.name}")

        model = Tags()
        model.name = item["name"]
        model.title = item["title"]
        model.color = item.get_color()
        model.desc = item["title"]
        model.tag_media = 'example.png'
        model.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with session_scope() as session:
            session.add(model)
            session.commit()
        return item