#!/usr/bin/env python3

from __future__ import print_function
import sys
import numpy as np
import ujson as json
import Levenshtein
import difflib
import time

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

comment_post_time = {}
author_avg_resp_time = {}
distinct_subreddits = {}
distinct_posts = {}

counter = 0
for line in sys.stdin:
    j = json.loads(line)

    # Output progress to STDERR
    counter+=1
    if not counter % 1000000: eprint(time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.gmtime(j['created_utc'])))

    comment_post_time[j['id']] = j['created_utc']
    author = j['author']
    if j['parent_id'][:2] == "t1" and j['parent_id'][3:] in comment_post_time:
        response_time = j['created_utc'] - comment_post_time[j['parent_id'][3:]]
        if not author in author_avg_resp_time:
            author_avg_resp_time[author] = {}
            author_avg_resp_time[author]['count'] = 1
            author_avg_resp_time[author]['sum'] = response_time
            author_avg_resp_time[author]['length'] = len(j['body'])
            distinct_subreddits[author] = set([j['subreddit']])
            distinct_posts[author] = set([j['link_id']])
            author_avg_resp_time[author]['last_body'] = j['body']
            author_avg_resp_time[author]['levenshtein'] = 0
            author_avg_resp_time[author]['ratcliff'] = 0
        else:
            author_avg_resp_time[author]['count'] += 1
            author_avg_resp_time[author]['sum'] += response_time
            author_avg_resp_time[author]['length'] += len(j['body'])
            distinct_subreddits[author].add(j['subreddit'])
            distinct_posts[author].add(j['link_id'])
            author_avg_resp_time[author]['levenshtein'] += Levenshtein.ratio(author_avg_resp_time[author]['last_body'], j['body'])
            author_avg_resp_time[author]['ratcliff'] += difflib.SequenceMatcher(None,author_avg_resp_time[author]['last_body'],j['body']).ratio()
            author_avg_resp_time[author]['last_body'] = j['body']

sorted_list = sorted(author_avg_resp_time, key=lambda x: (author_avg_resp_time[x]["sum"] / author_avg_resp_time[x]["count"]))
for author in sorted_list:
    if author_avg_resp_time[author]['count'] > 10:
        avg_reply_time = round(author_avg_resp_time[author]['sum'] / author_avg_resp_time[author]['count'],2)
        total_comments = author_avg_resp_time[author]['count']
        total_unique_subreddits = len(distinct_subreddits[author])
        total_unique_submissions = len(distinct_posts[author])
        avg_comment_length = round(author_avg_resp_time[author]['length'] / author_avg_resp_time[author]['count'],2)
        levenshtein_ratio = round(author_avg_resp_time[author]['levenshtein'] / (author_avg_resp_time[author]['count']-1),2)
        radcliff_ratio = round(author_avg_resp_time[author]['ratcliff'] / (author_avg_resp_time[author]['count']-1),2)
        print (avg_reply_time, total_comments, total_unique_subreddits, total_unique_submissions, avg_comment_length, levenshtein_ratio, radcliff_ratio, author, sep=", ")
