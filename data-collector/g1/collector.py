from uuid import uuid4
import requests as req
import json
import re
import sys

news=sys.argv[1]
comment_sample = '{id};{content};{likes};{dislikes};{reply_to};{news_id};{news_title};{news_link}\n'

def remove_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def retrieve_news_title_from_link(link):
    return link.split('/')[-1].strip('.ghtml').replace('-', ' ').capitalize()

def format_comment_to_csv(comment, parent=None):
    node = comment.get('node')
    comment_data = comment_sample.format(
        id=node.get('id'),
        content=remove_html(node.get('body')).replace(';','.'),
        likes=int(node.get('actionCounts').get('reaction').get('total')),
        dislikes=0,
        reply_to=parent if parent else '',
        news_id=news_id,
        news_title=news_title,
        news_link=news_link
    )

    return comment_data


with open('./urls/{}.txt'.format(news), 'r') as f:
    lines = f.readlines()

with open('../../collected-data/{}-comments.csv'.format(news),'w') as fp:
    for url in lines:
        response = req.get(url)
        body = json.loads(response.text).get('data')
        news_id = body.get('settings').get('id')
        news_link = body.get('story').get('url')
        news_title = retrieve_news_title_from_link(body.get('story').get('url'))
        comments = body.get('story').get('comments').get('edges')
        for comment in comments:
            fp.write(format_comment_to_csv(comment))
            node = comment.get('node')
            content = remove_html(node.get('body')).replace(';', '.')
            for reply in node.get('replies').get('edges'):
                fp.write(format_comment_to_csv(reply, parent=content))
