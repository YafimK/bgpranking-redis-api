#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
    Micro-blog
    ~~~~~~~~~~

    Microblog client for twitter

"""

import twitter
import datetime
import dateutil

from micro_blog_keys import twitter_consumer_key,twitter_consumer_secret,\
        twitter_access_key,twitter_access_secret
import bgpranking

api = None
username = "bgpranking"

def __prepare():
    global api
    api = twitter.Api(consumer_key=twitter_consumer_key,
            consumer_secret=twitter_consumer_secret,
            access_token_key=twitter_access_key,
            access_token_secret=twitter_access_secret)

def prepare_string():
    to_return = 'Top Ranking {date}\n'.format(
            date=datetime.date.today().isoformat())
    top = bgpranking.cache_get_top_asns(limit=5, with_sources=False)
    for asn, descr, rank in top['top_list']:
        rank = round(1+rank, 4)
        to_return += '{asn}: {rank}\n'.format(asn=asn, rank=rank)
    to_return += 'http://bgpranking.circl.lu'
    return to_return

def post_new_top_ranking():
    posted = False
    today = datetime.date.today()
    status = api.GetUserTimeline("bgpranking", count=100)
    for s in status:
        t = s.text
        if t is not None and t.startswith('Top Ranking'):
            most_recent_post = dateutil.parser.parse(
                    s.created_at).replace(tzinfo=None).date()
            if most_recent_post < today:
                posted = True
                to_post = prepare_string()
                api.PostUpdate(to_post)
            break
    return posted
