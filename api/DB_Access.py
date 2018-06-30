# all function for db access

import sqlite3
import datetime
from flask import session, g
from .utils import sql_row_to_dict


def search_entry(id):
    """Search entry by id. Returns a dict with all entry information"""
    query = "SELECT * FROM posts WHERE id = :id"
    c = g.db.execute(query, {'id': str(id)})
    row = c.fetchone()
    if row is None:
        return {"Error": "EntryNotFound"}
    return sql_row_to_dict(c, row)


def add_entry(entryRequest):
    """Add an enrty into the DB."""

    query = '''INSERT INTO posts(content, creation_date, creator_username, upvotes, downvotes) 
    VALUES(:content, datetime('now'), :creator_username, 0, 0)'''  # content, creation date, and username are given within the request. up/down votes get defult value of 0.

    parameters = {'content': entryRequest['content'],
                  'creator_username': session['username']}

    g.db.execute(query, parameters)
    g.db.commit()

    return True


def delete_entry(id):
    query = '''DELETE FROM posts WHERE id = :id'''
    parameters = {'id': id}

    g.db.execute(query, parameters)
    g.db.commit()


def add_user(user_name, password):
    query = '''
    INSERT INTO users(username, password) 
        VALUES(:name, :password)'''

    parameters = {'name': user_name, 'password': password}

    g.db.execute(query, parameters)
    g.db.commit()


def search_user(username):
    query = '''SELECT password FROM users WHERE username = :name '''
    parameters = {'name': username}

    c = g.db.execute(query, parameters)
    password = c.fetchone()
    if password is None:
        return {}
    return sql_row_to_dict(c, password)


def verify_entry_creator(id, username):
    query = '''SELECT creator_username FROM posts WHERE id = :id'''
    parameters = {'id': id}

    c = g.db.execute(query, parameters)
    user = c.fetchone()
    if user is None:
        return 'EntryNotFound'
    if user[0] != username:
        return 'UpdateNotAllowed'
    return''


def update_entry_content(id, content):
    """update a post at id with the content provided. IMPORTANT: this assumes the post exist, and would not notify you other wise."""
    query = '''UPDATE posts SET content = :content WHERE id = :id'''
    parameters = {'content': content['content'], 'id': id}

    g.db.execute(query, parameters)
    g.db.commit()


def update_entry_upvote(id, is_upvote, change_value):
    if is_upvote:
        query = 'UPDATE posts SET upvotes = upvotes + ' + str(change_value) + ' WHERE id = :id'
    else:
        query = 'UPDATE posts SET downvotes = downvotes + ' + str(change_value) + ' WHERE id = :id'


    paramters = {'id': id}
    g.db.execute(query, paramters)
    g.db.commit()


def get_vote(username, entryID):
    query = '''SELECT is_upvote FROM upvotes WHERE entry_id = :entryID AND username = :username'''
    parameters = {'entryID': entryID, 'username': username}

    c = g.db.execute(query, parameters)
    result = c.fetchone()
    if result is None:
        return result
    return sql_row_to_dict(c, result)


def add_vote(username, entryID, is_upvote):
    """Add an upvote/downvote to the table. IMPORTANT: this HAS to get an existing usernamd and an existing entry id!"""
    query = '''INSERT INTO upvotes(username, entry_id, is_upvote) VALUES(:username, :entryID, :is_upvote)'''
    parameters = {'entryID': entryID, 'username': username, 'is_upvote': is_upvote}
    try:
        g.db.execute(query, parameters)
        g.db.commit()
        return ''
    except:
        return 'UpvoteError'


def delete_vote(username, entryID):
    query = '''DELETE FROM upvotes WHERE entry_id = :entryID and username = :username'''
    parameters = {'entryID': entryID, 'username': username}

    g.db.execute(query, parameters)
    g.db.commit()


def update_vote(username, entryID, is_upvote):
    query = '''UPDATE upvotes SET is_upvote = :is_upvote WHERE entry_id = :entryID and username = :username'''
    parameters = {'is_upvote': is_upvote, 'entryID': entryID, 'username': username}

    g.db.execute(query, parameters)
    g.db.commit()


def get_all_most_voted_from_cache():
    """this fetces all of the most voted table, which is updated once every few miniutes"""
    query = '''SELECT * FROM most_voted'''
    c = g.db.execute(query)
    posts = {}
    counter = 0
    for row in c.fetchall():
        counter += 1
        posts[str(counter)] = sql_row_to_dict(c, row)
    return posts


def search_most_voted_cache(id):
    """check if a post is in the cache"""
    query = '''SELECT * FROM most_voted WHERE id = :id'''
    parameters = {'id': id}
    c = g.db.execute(query, parameters)
    if c.fetchone() is None:
        return False
    return True


def get_most_voted_from_table(number_of_records, maximum_age):
    query = '''SELECT * FROM posts WHERE datetime('now') - datetime(creation_date) <= :maximum_age 
        ORDER BY upvotes - downvotes DESC LIMIT :number'''
    parameters = {'number': number_of_records, 'maximum_age': maximum_age}
    c = g.db.execute(query, parameters)
    posts = {}
    counter = 0
    for row in c.fetchall():
        counter += 1
        posts[str(counter)] = sql_row_to_dict(c, row)
    return posts


def add_to_most_voted_cache(new_post, old_post):
        query = '''DELETE FROM most_voted WHERE id = :entryID'''
        parameters = {'entryID': old_post['id']}
        g.db.execute(query, parameters)
        g.db.commit()

        query = '''INSERT INTO most_voted(id, content, creation_date, creator_username, upvotes, downvotes) 
    VALUES(:id, :content, :date, :creator_username, :upvotes, :downvotes)'''
        parameters = {'id': new_post['id'], 'content': new_post['content'],
                      'date':new_post['creation_date'], 'creator_username': new_post['creator_username'], 'upvotes': new_post['upvotes'], 'downvotes': new_post['downvotes']}  # this logs the total amount of upvotes (with downvotes included)
        g.db.execute(query, parameters)
        g.db.commit()


def update_cache_vote(post, id):
    query = '''UPDATE most_voted SET upvotes = :upvotes WHERE id = :id'''
    parameters = {'upvotes': post['upvotes'] - post['downvotes'], 'id': id} # this logs the total amount of upvotes (with downvotes included)
    g.db.execute(query, parameters)
    g.db.commit()


def least_voted_in_cache():
    """gives you the least voted post in the cache to check if it needs to be updated."""
    query = '''SELECT * FROM most_voted ORDER BY upvotes - downvotes ASC LIMIT 1 '''
    c = g.db.execute(query)
    result = c.fetchone()
    print(result)
    if result is None:
        return result
    return sql_row_to_dict(c, result)


def refresh_to_most_voted_cache(posts):
    query = '''DELETE FROM most_voted'''
    g.db.execute(query)
    g.db.commit()
    for key, post in posts.items():
        query = '''INSERT INTO most_voted(id, content, creation_date, creator_username, upvotes, downvotes) 
    VALUES(:id, :content, :date, :creator_username, :upvotes, :downvotes)'''
        parameters = {'id': post['id'], 'content': post['content'],
                      'date': post['creation_date'], 'creator_username': post['creator_username'], 'upvotes': post['upvotes'], 'downvotes': post['downvotes']}  # this logs the total amount of upvotes (with downvotes included)
        g.db.execute(query, parameters)
        g.db.commit()


