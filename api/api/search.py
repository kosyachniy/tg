from mongodb import db
from api._error import ErrorWrong
from func.tg_user import search as tg_search



def get_xml(i, inp):
    el = {
        'ID': i.id,

        # 'Header': '',
        'Body': i.message,

        # 'Username': '',
        'Userlink': i.to_id.channel_id,

        # 'Hashtags': [],

        'Date': i.date.timestamp(),

        'Keyword': inp,

        'Details': {
            'Emotions': {
                'Views': i.views,
                # 'Likes': 0,
                # 'Dislikes': 0,
            },
        },
    }

    return el

def get_json(i, inp):
    el = {
        'id': i.id,

        # 'name': ,
        'cont': i.message,

        # 'author': {},

        'source': {
            'id': i.to_id.channel_id,
        },

        'tag': inp,

        'time': int(i.date.timestamp()),
    }

    if i.views:
        el['reactions'] = {
            'views': {
                'count': i.views,
            },
        }

    return el


def search(discussion_id):
    db_filter = {
        '_id': False,
        'tags': True,
    }

    discussion = db['discussions'].find_one({'id': discussion_id}, db_filter)

    if not discussion:
        raise ErrorWrong('id')

    tags = discussion['tags']

    for tag in tags:
        for post in tg_search(tag):
            # message = {
            #     'tg_id': post.id,
            #     'source': post.to_id.channel_id,
            #     'cont': post.message,
            #     'time': post.date.timestamp,
            #     'reactions': {
            #         'views': {
            #             'count': post.views,
            #         }
            #     }
            # }

            message = get_json(post, tag)
            print(message)