from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', minute='*/25')
def scheduled_job():
    url = "https://drivingcar.herokuapp.com/"
    conn = requests.get(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()