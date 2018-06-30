# Run this first to start the server

import os
from api.Microblog import app
from apscheduler.schedulers.background import BackgroundScheduler
import api.Votes as Votes


class APScheduler(BackgroundScheduler):
    def run_job(self, id, jobstore=None):
        print ("this")
        with self.app.app_context():
            super().run_job(id=id, jobstore=jobstore)


if __name__ == '__main__':
    app.debug = True
    app.config['DATABASE_NAME'] = 'Database.db'
    app.secret_key = "password"
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))

    #sched = APScheduler(daemon=True)
    #sched.add_job(Votes.update_most_upvoted_cache, 'interval', seconds=Votes.TIME_TO_UPDATE_CACHE)
    #sched.start()

    app.run(host=host, port=port)