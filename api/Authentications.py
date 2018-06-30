from .Users import verify_user


# templates for authanticating post request. defining name of parameter and type.
request_templates = {
    'EntryPost': {'content': (str)},
    'UserPost': {'username': (str), 'password': (str)},
    'UpdatePost': {'content': (str), 'upvote': bool}
    }


def authenticate_post_request(request, request_type):
    """check if the request contains all nessercery parameters and that all parameters are of the correct type, using a given tempalte"""
    if request_type == "UpdatePost":
        return auth_update_request(request)  # see explantion below.

    if request_type not in request_templates.keys():
        print ("Request type doesn't exist")
        return False
    template = request_templates[request_type]
    for key in template.keys():
        if key not in request.keys():
            return "ParametersMissing"
        if not isinstance(request[key], template[key]):
            return "WrongParameters"
    return ''

def auth_update_request(request):
    """Authanticate an update request. this is a special function, because update requests
    only demend one of three keys (and not all keys in the template).
    update could be a content update (which requiers user authantication),
    an upvote or a down vote, and should, in practice, only include one."""
    template = request_templates["UpdatePost"]
    keys_found = []
    for key in template:
        if key in request:
            keys_found.append(key)
    if len(key) == 0:
        return "ParametersMissing"
    for k in keys_found:
        if not isinstance(request[k], template[k]):
            return "WrongParameters"
    return ''

def authanticate_user(request):
    """checks for basic auth data in the request. This should be called by all request function who requier a user to be logged in."""
    if request.authorization is None:
        return 'LoginRequierd'
    #checking for a cookie goes here
    if 'username' not in request.authorization or 'password' not in request.authorization:
        return 'LoginRequierd'
    username = request.authorization['username']
    password = request.authorization['password']
    if username is None or password is None:
        return 'LoginRequierd'

    return verify_user(username, password)
