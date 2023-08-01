#!/usr/bin/python
# -*- coding: utf-8 -*-

from xiezhen import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Time, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from contextlib import contextmanager


engine = create_engine(f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB_NAME}", pool_recycle=3600)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        #session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    post_live = Column(Boolean)
    post_instant = Column(String(51))
    post_color = Column(String(91))
    post_desc = Column(Text)
    post_title = Column(String(191))
    post_slug = Column(String(191))
    post_media = Column(Text)
    post_video = Column(Text)
    video_url = Column(Text)
    edit_id = Column(Integer)
    media_alt = Column(Text)
    counter = Column(Integer)
    origin_link = Column(String(200))
    origin_created_at = Column(String(32))
    created_at = Column(String(32))
    updated_at = Column(String(32))

class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    title = Column(String(191))
    name = Column(String(191))
    tag_media = Column(String(191))
    color = Column(String(31))
    desc = Column(String(191))
    created_at = Column(String(32))
    updated_at = Column(String(32))

class Post_Tag(Base):
    __tablename__ = 'post_tag'
    post_id = Column(Integer, primary_key = True)
    tag_id = Column(Integer, primary_key = True)


class Contents(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    embed_id = Column(Integer)
    _type = Column("type", String(191))
    body = Column(Text)
    extra = Column(Text)