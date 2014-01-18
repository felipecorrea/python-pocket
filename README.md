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

Run the **get_access_token.py** tool to obtain an Authentication token for API calls.

In order to create an instance of the pocket.API with login credentials, run:

```
>>> import pocket
>>> api = pocket.Api(consumer_key='consumer_key',
                     access_token='access_token')
```

### Adding Items to Pocket

**Required Permissions**: In order to use the /v3/add endpoint, your consumer key must have the "Add" permission.

To add an Item to your Pocket list:

```
>>> item = api.add('https://www.google.com/culturalinstitute/exhibit/nelson-mandela-negotiating-for-democracy/gRl9f-1K')
>>> print item.id
>>> print item.title
```

### Modifying a User's Pocket Data

**Required Permissions**: In order to use the /v3/send endpoint, your consumer key must have the "Modify" permission.

To batch several actions to a user's changes, run:

```
>>> actions = api.send('[
    {
        "action" : "archive",
        "item_id" : "229279689",
        "time"   : "1348853312"
    }
]')
>>> for action in actions:
         print (action)
```

You can send one action or you can send dozens. The list of actions should be sent as a JSON array. The response you receive back contains a list that indicates which action had an issue if the status is False (indicating failure).

#### List of actions

**Basic Actions**

- [add](http://getpocket.com/developer/docs/v3/modify#action_add): Add a new item to the user's list.
- [archive](http://getpocket.com/developer/docs/v3/modify#action_archive): Move an item to the user's archive.
- [readd](http://getpocket.com/developer/docs/v3/modify#action_readd): Re-add (unarchive) an item to the user's list.
- [favorite](http://getpocket.com/developer/docs/v3/modify#action_favorite): Mark an item as a favorite.
- [unfavorite](http://getpocket.com/developer/docs/v3/modify#action_unfavorite): Remove an item from the user's favorites.
- [delete](http://getpocket.com/developer/docs/v3/modify#action_delete): Permanently remove an item from the user's account.

**Tagging Actions**

- [tags_add](http://getpocket.com/developer/docs/v3/modify#action_tags_add): Add one or more tags to an item.
- [tags_remove](http://getpocket.com/developer/docs/v3/modify#action_tags_remove): Remove one or more tags from an item.
- [tags_replace](http://getpocket.com/developer/docs/v3/modify#action_tags_replace): Replace all of the tags for an item with one or more provided tags.
- [tags_clear](http://getpocket.com/developer/docs/v3/modify#action_tags_clear): Remove all tags from an item.
- [tag_rename](http://getpocket.com/developer/docs/v3/modify#action_tag_rename): Rename a tag; this affects all items with this tag.

### Retrieving a User's Pocket Data

**Required Permissions**: In order to use the /v3/get endpoint, your consumer key must have the "Retrieve" permission.

To get the user's Pocket list, run:

```
>>> items_list = api.get()
>>> for item in items_list:
         print "%s (%s)" % (item.title, item.resolved_url)
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
