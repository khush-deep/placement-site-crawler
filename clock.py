from apscheduler.schedulers.blocking import BlockingScheduler
import app, os

sched = BlockingScheduler()

def scheduled_job():
    app.main()

sched.add_job(scheduled_job, 'cron', hour='0-23/2')
sched.start()