from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from celery.signals import task_revoked, task_success, task_failure
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import time
from .some_work import Work
from .extras.Login_Automation import kite_login

# this decorator is all that's needed to tell celery this is a worker task
@task(bind=True)
def do_work(self, user_pk):  
    # time.sleep(2)
    w = Work(self, user_pk)
    w.run()
    

@task_revoked.connect
def on_task_revoked(*args, **kwargs):
    # print(str(kwargs))
    print('### some task_revoked')


# @periodic_task(run_every=crontab(hour=8, minute=30))
# @periodic_task(run_every=crontab())
def daily_kite_login():
	print('Starting daily login')
	# kite_login()
	# print("logged into KITE!")
    


# celery -A periodic beat --loglevel=info
# celery -A prj worker --beat --scheduler django --loglevel=info
"""

#Reading the stated
from celery.result import AsyncResult
result = AsyncResult(task_id)
print(result.state)  # will be set to PROGRESS_STATE
print(result.info)  # metadata will be here


Solution to error :- JSON dumps
Another working solution is to use eventlet (`pip install eventlet` ->
`celery -A your_app_name worker --pool=eventlet`).
This way it is possible to have parallel-running tasks on Windows.

"""