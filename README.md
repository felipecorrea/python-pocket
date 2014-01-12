# Python Pocket

**A Python wrapper around the Pocket API.**

Author: Felipe Borges <felipe10borges@gmail.com>

## Introduction

This library provides a pure Python interface for the [Pocket API](http://getpocket.com/developer/).

[Pocket](http://getpocket.com) lets you take your content with you. Whenever you come across an interesting article, video, or website you want to check out later, you no longer have to send yourself links or bookmark items in your browser. Simply put it in your Pocket. 

## Building

Install the dependencies:

- [SimpleJson](http://cheeseshop.python.org/pypi/simplejson)

Get the code:

```
git clone https://github.com/felipeborges/python-pocket
```

And run:

```
$ cd python-pocket
$ python setup.py build
$ python setup.py install
```

## Using

**get_access_token.py**: Is a tool to obtain an Authentication token for API calls.

To create an instance of the pocket.API with login credentials, run:

```
>>> import pocket
>>> api = pocket.Api(consumer_key='consumer_key',
                     access_token='access_token')
```

To add an Item to your Pocket list:

```
>>> item = api.add('https://www.google.com/culturalinstitute/exhibit/nelson-mandela-negotiating-for-democracy/gRl9f-1K')
>>> print item.id
>>> print item.title
```

To get the user's Pocket list, run:

```
>>> items_list = api.get()
>>> for item in items_list:
>>>     print "%s (%s)" % (item.title, item.resolved_url)
```

A few examples of the types of requests you can make:

- Retrieve a user's list of unread items.
- Sync data that has changed since the last time your app checked.
- Retrieve paged results sorted by the most recent saves.
- Retrieve just videos that the user has saved.
- Search for a given keyword in item's title and url.
- Retrieve all items for a given domain.

You can filter the **get()** results by passing these parameters:

- **state** = 'unread', 'archive' or 'all'.
- **favorite** = '0' or '1' to return un-favorited items or favorite items respectively.
- **tag** = 'tag-name' or '_untagged_'.
- **contentType** = 'article', 'video' or 'image'.
- **sort** = 'newest', 'oldest', 'title' or 'site'.
- **detailType** = 'simple' or 'complete'.

Run _pydoc pocket.Api.get_ to obtain more info.

## Todo

- pip install
- modify & retrieve methods

## License

```
Copyright 2014 Felipe Borges

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
