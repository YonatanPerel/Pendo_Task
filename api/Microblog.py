import json
from flask_restful import Resource, Api
from flask import Flask, abort, request, g, session
from .utils import *
from .Authentications import *
from .DB_Access import *
from .Users import verify_user, create_new_user
from .Errors import *
from .Votes import *

app = Flask(__name__)
api = Api(app, errors = errors)



@app.before_request
def before_request():
    g.db = sqlite3.connect(app.config['DATABASE_NAME'])
    if 'logged_in' not in session:
        session['isLoggedin'] = False
    if 'username' not in session:
        session['username'] = ''


class BlogEntryResource(Resource):
    def get(self, id):
        entry = search_entry(id)
        if 'Error' in entry:
            raise_costume_abort(entry['Error'])
        return json_response(json.dumps(entry))

    def delete(self, id):
        auth_check = authanticate_user(request)  # check if user exists
        if auth_check != "":
            raise_costume_abort(auth_check)

        auth_check = verify_entry_creator(id, session['username'])  # check if user is the creator of the post.
        if auth_check != "":
            raise_costume_abort(auth_check)

        delete_entry(id)
        return json_response('', status=200)

    def post(self, id):
        auth_check = authanticate_user(request)  # check if user exists
        if auth_check != "":
            raise_costume_abort(auth_check)
        content = request.json
        auth_check = authenticate_post_request(content, "UpdatePost")
        if auth_check != '':
            raise_costume_abort(auth_check)
        if 'content' in content:
            auth_check = verify_entry_creator(id, session['username'])
            if auth_check != '':
                raise_costume_abort(auth_check)
            update_entry_content(id, content)
        if 'upvote' in content:
            handle_voting(session['username'], id, content['upvote'])
        return(json_response('', status = 200))


class BlogEntriesListResource(Resource):
    def get(self):
        posts = get_all_most_voted_from_cache()
        return json_response(json.dumps(posts))

    def post(self):
        auth_check = authanticate_user(request)  # check if user exists
        if auth_check != "":
            raise_costume_abort(auth_check)
        entry = request.json
        auth_check = authenticate_post_request(entry, 'EntryPost')
        if auth_check != '':
            raise_costume_abort(auth_check)
        add_entry(entry)
        return json_response('', status=201)


class UserLoginResource(Resource):
    def post(self):
        user = request.json
        auth_check = authenticate_post_request(user, 'UserPost')
        if auth_check != '':
            raise_costume_abort(auth_check)
        auth_check = verify_user(user['username'], user['password'])
        if auth_check != '':
            raise_costume_abort(auth_check)
        return json_response('')


class UserSignUpResource(Resource):
    def post(self):
        user = request.json
        auth_check = authenticate_post_request(user, 'UserPost')
        if auth_check != '':
            raise_costume_abort(auth_check)
        auth_check = create_new_user(user['username'], user['password'])
        if auth_check != '':
            raise_costume_abort(auth_check)
        return json_response('')


api.add_resource(BlogEntryResource, '/entry/<int:id>')
api.add_resource(BlogEntriesListResource, '/entry')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserSignUpResource, '/signup')


