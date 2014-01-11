#!/usr/bin/env python
#
# vim: sw=4 ts=4 st=4
#
#  Copyright 2014 Felipe Borges <felipe10borges@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''A library that provides a Python interface to the Pocket API'''

__author__ = 'felipe10borges@gmail.com'
__version__ = '0.1'

import urllib
import urllib2
import simplejson
import sys

class ItemsList(object):
    '''A Class representing a user's Pocket list.'''
    def __init__(self, items, status = None):
        self._items = items
        self.status = status

    def __getitem__(self, item_id):
        return self._items[item_id]

    def __iter__(self):
        for item in self._items.items():
            yield item[1]

    def __len__(self):
        return len(self._items.items())

    def get_item_by_id(self, item_id):
        return self._items[item_id]

class Item(object):
    '''A Class representing a saved item.

    The Item structure exposes the folowing properties:

        item.id
        item.normal_url
        item.resolved_id
        item.resolved_url
        item.domain_id
        item.origin_domain_id
        item.response_code
        item.mime_type
        item.content_length
        item.encoding
        item.date_resolved
        item.date_published
        item.title
        item.excerpt
        item.word_count
        item.has_image
        item.has_video
        item.is_index
        item.is_article
        item.authors
        item.images
        item.videos
    '''
    def __init__(self, **kwargs):
        param_defaults = {
            'id' : None,
            'normal_url' : None,
            'resolved_id' : None,
            'resolved_url' : None,
            'domain_id' : None,
            'origin_domain_id' : None,
            'response_code' : None,
            'mime_type' : None,
            'content_length' : None,
            'encoding' : None,
            'date_resolved' : None,
            'date_published' : None,
            'title' : None,
            'excerpt' : None,
            'word_count' : None,
            'has_image' : None,
            'has_video' : None,
            'is_index' : None,
            'is_article' : None,
            'authors' : None,
            'images' : None,
            'videos' : None,
        }

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

class PocketError(Exception):
    def __init__(self, reason, response = None):
        self.reason = unicode(reason)
        self.response = response

    def __str__(self):
        return self.reason

class Api(object):
    METHOD_URL = 'https://getpocket.com/v3/'
    REQUEST_HEADERS = { 'X-Accept': 'application/json' }

    ''' Pocket API '''
    def __init__(self, consumer_key = None, access_token = None):
        if consumer_key is not None and access_token is None:
            print >> sys.stderr, 'Pocket requires an Authentication Token for API calls.'
            print >> sys.stderr,  'If you are using this library from a command line utility, please'
            print >> sys.stderr,  'run the included get_access_token.py tool to generate one.'

            raise PocketError('Pocket requires an Authentication Token for all API access')

        self.set_credentials(consumer_key, access_token)

    def set_credentials(self, consumer_key, access_token):
        self._consumer_key = consumer_key
        self._access_token = access_token

    def _create_request(self, method, params):
        return urllib2.Request(Api.METHOD_URL + method, urllib.urlencode(params), Api.REQUEST_HEADERS)

    def add(self, url, title = None, tags = None, tweet_id = None):
        '''Add a Single Item to a user's Pocket list

        Args:
            url:
                The URL of the item you want to save.
            title:
                This can be included for cases where an item does not have a 
                title, which is typical for image or PDF URLs. If Pocket detects
                a title from the content of the page, this parameter will be 
                ignored.
            tags:
                A comma-separated list of tags to apply to the item.
            tweet_id:
                A reference to the tweet status id. This allows Pocket to show 
                the original tweet alongside the article.

        Returns:
            A pocket.Item instance.
        '''
        params = {
            'consumer_key' : self._consumer_key,
            'access_token' : self._access_token,
            'url' : url
        }

        if title is not None:
            params['title'] = title

        if tags is not None:
            tag_str = ''
            for tag in tags:
                tag_str += tag + ','

            params['tags'] = tag_str

        if tweet_id is not None:
            params['tweet_id'] = tweet_id

        request = self._create_request('add', params)

        try:
            resp = urllib2.urlopen(request)
        except Exception, e:
            raise PocketError(e)

        json_response = simplejson.loads(resp.read())

        return self.new_item_from_json_dict(json_response)

    @staticmethod
    def new_item_from_json_dict(data):
        '''Create a new instanced based on a JSON dict.

        Args:
            data:
                A JSON dict, as converted from the JSON in the Pocket API

        Returns:
            A pocket.Item instance
        '''
        item = data['item']
        status = data['status']

        return Item(id = item.get('id'),
                    normal_url = item.get('normal_url'),
                    resolved_id = item.get('resolved_id'),
                    resolved_url = item.get('resolved_url'),
                    domain_id = item.get('domain_id'),
                    origin_domain_id = item.get('origin_domain_id'),
                    response_code = item.get('response_code'),
                    mime_type = item.get('mime_type'),
                    content_length = item.get('content_length'),
                    encoding = item.get('encoding'),
                    date_resolved = item.get('date_resolved'),
                    date_published = item.get('date_published'),
                    title = item.get('title'),
                    excerpt = item.get('excerpt'),
                    word_count = item.get('word_count'),
                    has_image = item.get('has_image'),
                    has_video = item.get('has_video'),
                    is_index = item.get('is_index'),
                    is_article = item.get('is_article'),
                    authors = item.get('authors'),
                    images = item.get('images'),
                    videos = item.get('videos'))

    def get(self, **kwargs):
        '''Retrieve item(s) from a user's Pocket list.

        A few examples of the types of requests you can make:
            - Retrieve a user's list of unread items.
            - Sync data that has changed since the last time your app checked.
            - Retrieve paged results sorted by the most recent saves.
            - Retrieve just videos that the user has saved.
            - Search for a given keyword in item's title and url.
            - Retrieve all items for a given domain.

        Args:
            state:
                'unread': only return unread items (default).
                'archive': only return archived items.
                'all': return both unread and archived items.
            favorite:
                '0': only return un-favorited items.
                '1': only return favorited items.
            tag:
                'tag_name': only return items tagged with tag_name.
                '_untagged_': only return untagged items.
            contentType:
                'article': only return articles
                'video': only return videos or articles with embedded videos.
                'image': only return images.
            sort:
                'newest': return items in order of newest to oldest.
                'oldest': return items in order of oldest to newest.
                'title': return items in order of title alphabetically.
                'site': return items in order of url alphabetically.
            detailType:
                'simple': only return the titles and urls of each item.
                'complete': return all data about each item, including tags,
                images, authors, videos and more.
        Returns:
            A pocket.ItemsList instance.
        '''
        param_defaults = {
            'state' : None,
            'favorite' : None,
            'tag' : None,
            'contentType' : None,
            'sort' : None,
            'detailType' : None,
            'search' : None,
            'domain' : None,
            'since' : None,
            'count' : None,
            'offset' : None,
        }

        params = {
            'consumer_key' : self._consumer_key,
            'access_token' : self._access_token
        }

        for (param, default) in param_defaults.iteritems():
            if kwargs.get(param, default) is not None:
                params[param] = kwargs.get(param, default)

        request = self._create_request('get', params)

        try:
            resp = urllib2.urlopen(request)
        except Exception, e:
            raise PocketError(e)

        json_response = simplejson.loads(resp.read())

        return self.new_items_list_from_json_dict(json_response)

    @staticmethod
    def new_items_list_from_json_dict(data):
        status = data['status']
        items_list = {}

        for item in data['list'].items():
            items_list[item[1].get('item_id')] = (Item(id = item[1].get('item_id'),
                                                       resolved_id = item[1].get('resolved_id'),
                                                       resolved_url = item[1].get('resolved_url'),
                                                       title = item[1].get('resolved_title'),
                                                       excerpt = item[1].get('excerpt'),
                                                       is_article = item[1].get('is_article'),
                                                       has_image = item[1].get('has_image'),
                                                       has_video = item[1].get('has_video'),
                                                       word_count = item[1].get('word_count'),
                                                       authors = item[1].get('authors'),
                                                       images = item[1].get('images'),
                                                       videos = item[1].get('videos')))

        return ItemsList(items_list, status)
