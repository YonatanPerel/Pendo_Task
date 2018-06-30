from flask_restful import HTTPException

# this are all the costume errors the server can respond with. the key is the error name, sent to a function to render a response.

errors = {
    'EntryNotFound': {
        'message': 'could not find blog entry',
        'status': 404,
    },
    'UserAlreadyExists': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'UserNotFound':{
        'message': 'wrong username or password',
        'status': 403
    },
    'ParametersMissing': {
        'message': 'Parameters missing from response',
        'status': 400,
    },
    'WrongParameters': {
        'message': "Parameters are not of the correct format",
        'status': 400,
    },
    'LoginRequierd': {
        'message': "Logging in is requierd for the request you were trying to make.",
        'status': 405,
    },
    'UpdateNotAllowed': {
        'message': "You cannot update or delete someone elses posts.",
        'status': 401,
    },
    'UpvoteError': {
        'message': "Error trying to upvote the post. are you sure both the user and the blog entry exists?",
        'status': 404,
    }
}