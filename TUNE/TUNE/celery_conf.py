import os
from celery import Celery

from TUNE.settings import client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TUNE.settings')
app = Celery('TUNE')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     x = sender.add_periodic_task(30.0, admin_report.s(), name='ОТЧЕТ О ФИНАНСАХ')
#     print('----------------------------------------------------------------')
#
# @app.task
# def admin_report():
#     client.send_message(
#         chat_id=572982939,
#         text='12222222222'
#     )
