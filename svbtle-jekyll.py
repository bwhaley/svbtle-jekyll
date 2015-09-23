import re
import os
import sys
import argparse
from markdown import markdown
from bs4 import BeautifulSoup
import requests

svbtle_url = 'https://svbtle.com/'

def get_post_list(cookies):
    svbtle_dashboard = svbtle_url + 'dashboard'
    r = requests.get(svbtle_dashboard, cookies=cookies)
    soup = BeautifulSoup(r.content, 'html.parser')
    return [li.a['href'] for li in soup.select("li.published")]

def svbtle_parse(post, excerpt_length):
    svbtle = {}
    svbtle['title'] = post.find(id="post_title").contents[0].replace('\n', '')
    svbtle['content'] = post.find(id="post_content").contents[0]
    svbtle['excerpt'] = markdown(svbtle['content'])[0:excerpt_length] + "..."
    year = post.find(id="post_publish_date_1i").find_all(selected=True)[0].contents[0]
    month = post.find(id="post_publish_date_2i").find_all(selected=True)[0]['value']
    day = post.find(id="post_publish_date_3i").find_all(selected=True)[0].contents[0]
    svbtle['modified'] = '-'.join([year,month,day])
    return svbtle


def front_matter(**kwargs):
    return """---
layout: post
title: "{title}"
excerpt: "{excerpt}"
modified: {modified}
comments: true
---
""".format(**kwargs)


def jekyll_markdown(data):
    content = data['content'].replace('\r', '')
    return '\n'.join([front_matter(**data), content]).encode('utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Collect posts from Svbtle and output them in a Jekyll compatible markdown.")
    parser.add_argument('-c', '--cookie', help='Value of the remember_user_token cookie in the Svbtle account', required=True)
    parser.add_argument('-t', '--target', help='Target directory in which to render the posts in markdown', required=True)
    parser.add_argument('-l', '--excerpt-length', help='Number of characters to include in the excerpt', default=300)
    args = parser.parse_args()
    cookies = dict(remember_user_token=args.cookie)
    output_dir = args.target
    if not os.path.exists(output_dir):
        sys.exit("Target directory does not exist.")
    if not os.path.isdir(output_dir):
        sys.exit("Target directory is not a directory.")

    post_urls = get_post_list(cookies)

    for post_url in post_urls:
        #/my-post-url-example/edit
        r = requests.get(svbtle_url + post_url, cookies=cookies)
        svbtle_data = svbtle_parse(BeautifulSoup(r.text, 'html.parser'), args.excerpt_length)
        post_path = re.match('/([\w-]+)', post_url).group(1)
        jekyll_post = jekyll_markdown(svbtle_data)
        filename = svbtle_data['modified'] + '-' + post_path + '.md'
        with open('/'.join([output_dir, filename]), 'wb') as f:
            f.write(jekyll_post)
