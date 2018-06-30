from .DB_Access import *
from .utils import raise_costume_abort, int_to_bool, bool_to_int

CHANGE_VALUE_PER_VOTE = 1
NUMBER_OF_TOP_VOTES_TO_TRACK = 2
MAXIMUM_POST_AGE_IN_TABLE = 10  # in days.
TIME_TO_UPDATE_CACHE = 1  # in days.


def handle_voting(username, entryID, is_upvote):
    current_status = get_vote(username, entryID)
    if current_status is None:
        error = add_vote(username, entryID, bool_to_int(is_upvote))
        if error != '':
            raise_costume_abort(error)
        update_entry_upvote(entryID, is_upvote, CHANGE_VALUE_PER_VOTE)
        update_most_upvoted_cache(entryID, is_upvote)  # update the cache for the most voted.
        return ''

    current_status = int_to_bool(current_status['is_upvote'])

    if current_status == is_upvote:
        delete_vote(username, entryID)
        update_entry_upvote(entryID, is_upvote, -CHANGE_VALUE_PER_VOTE)
        update_most_upvoted_cache(entryID, is_upvote)  # update the cache for the most voted.
        return ''

    update_vote(username, entryID, is_upvote)
    update_entry_upvote(entryID, is_upvote, CHANGE_VALUE_PER_VOTE)
    update_entry_upvote(entryID, not is_upvote, -CHANGE_VALUE_PER_VOTE)
    update_most_upvoted_cache(entryID, is_upvote)  # update the cache for the most voted.
    return ''


def update_most_upvoted_cache(entry_id, is_upvote):
    """update the most voted table. the value of the upvotes per post is its upvotes minus its downvotes. this should run every minitue or so.."""
    new_in_cache = search_entry(entry_id)
    # if the post exist in cache, we only need to update the amount of upvotes it has.
    if search_most_voted_cache(entry_id):
        # if the post apeared in cache but was downvoted, we have to check the post db to make sure its still in the top votes.
        # this is easiest to do by refreshing the entire cache.
        if not is_upvote:
            resresh_most_upvoted_cache()
            return
        print("updating existing")
        update_cache_vote(new_in_cache, entry_id)
        return

    old_in_cache = least_voted_in_cache()
    #if the post is not in the cache, we check if it passed the least voted post already in the cche.
    #if it did, we delete that post and add the new one instead.
    print (new_in_cache)
    if new_in_cache['upvotes'] - new_in_cache['downvotes'] < old_in_cache['upvotes'] - old_in_cache['downvotes']:
        print("no need for an update")
        return

    add_to_most_voted_cache(new_in_cache, old_in_cache)


def resresh_most_upvoted_cache(db_path = ''):
    """Refresh the most voted cache. should happen once a day or so, to make sure all posts are not too old to apear in the cache."""
    print("refreshing cache...")
    if db_path != '':
        g.db = sqlite3.connect(db_path)  # when this runs on schedule (and not on request), it sets up its own db connection.
    table = get_most_voted_from_table(NUMBER_OF_TOP_VOTES_TO_TRACK, MAXIMUM_POST_AGE_IN_TABLE)
    refresh_to_most_voted_cache(table)
