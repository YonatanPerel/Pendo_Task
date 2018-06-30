# Run this first to start the server

import os
from api.Microblog import app
from flask_apscheduler import APScheduler
from api.Votes import TIME_TO_UPDATE_CACHE as minutes, resresh_most_upvoted_cache as update_votes


db_path = r'C:\Users\User\Desktop\microblog\Pendo_Task\Database.db'


def update_with_app_context():
    with app.app_context():
        update_votes(db_path)


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': update_with_app_context,
            'args': (),
            'trigger': 'interval',
            'minutes': minutes #  change this to set cache updating schedual. for debugging its set to 1 minute at the moment.
        }
    ]

if __name__ == '__main__':
    app.debug = True
    app.config['DATABASE_NAME'] = db_path
    app.config.from_object(Config())
    app.secret_key = "password"
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run(host=host, port=port)
